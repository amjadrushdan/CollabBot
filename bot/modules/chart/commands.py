import datetime
import discord
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from .module import module
from .data import tasklist
from .data import members
from io import BytesIO
from data import NULL
import numpy as np

@module.cmd(
    name="chart",
    desc="Create Gantt Chart based on your team todo list",
    group="Productivity",
    aliases=('charts','gantt'),
)
async def cmd_poll(ctx):
    """
    Usage:
        !chart
    Description:
        Create Gantt Chart based on your team todo list
    """
    # Retrieve task data from the tasklist based on specified criteria
    task = tasklist.select_where(
        channelid=ctx.ch.id,  # Filter tasks by channel ID
        deleted_at=NULL,  # Exclude tasks that are marked as deleted
        select_columns=(  # Select specific columns from the tasklist table
            'taskid',
            'userid',
            'content',
            'created_at',
            'deadline',
        ),
    )

    # Create a DataFrame with the required columns
    df_task = pd.DataFrame(task, columns=['taskid', 'userid', 'content', 'created_at', 'deadline'])

    # Extract unique userid values from the task DataFrame
    user_ids = df_task['userid'].unique()
    # Convert the user_ids array to a list
    user_ids = user_ids.tolist()

    # no task/user detected
    if len(user_ids) == 0:
        embed = discord.Embed(
            description="No task available . Use !todo to add task\n",
            colour=discord.Colour.orange(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name="{}".format(ctx.author.display_name),
            icon_url=ctx.author.avatar_url
            )
        await ctx.reply(embed=embed)
        
    else:
        member = members.select_where(
            userid=user_ids,
            guildid=ctx.guild.id,
            select_columns=(
            'userid',
            'display_name'
            )
        )
        # Create a DataFrame with the member data
        df_member = pd.DataFrame(member, columns=['userid', 'display_name'])

        # Merge the task and member DataFrames based on the 'userid' column
        df = pd.merge(df_task, df_member, on='userid', how='left')

        # Filter out rows with missing or invalid values
        df = df.dropna(subset=['created_at', 'deadline'])

        # Reset the index and drop the old index column
        df.reset_index(drop=True, inplace=True)
        
        if not df.empty:
            # Convert the relevant columns to datetimelike values
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['deadline'] = pd.to_datetime(df['deadline'])

            # Sort the DataFrame by the created_at column
            df.sort_values('created_at', inplace=True)

            # Set the x-axis limits based on the minimum of created_at and the maximum of deadline
            min_date = df['created_at'].min()

            # Calculate the number of days from project start to task start
            df['start_num'] = (df['created_at'] - min_date).dt.days

            # Calculate the number of days from project start to end of tasks
            df['end_num'] = (df['deadline'] - min_date).dt.days

            # Calculate the days between the start and end of each task
            df['days_start_to_end'] = df['end_num'] - df['start_num']

            # Set a minimum duration for tasks completed on the same day
            df['days_start_to_end'] = df['days_start_to_end'].apply(lambda x: max(x, 1))

            # Create a new column combining the index and task content
            df['task_label'] = df.index.astype(str) + ': ' + df['content']

            # Create a Gantt chart using the start_num and days_start_to_end columns
            fig, ax = plt.subplots(figsize=(16, 6))
            ax.grid(False)

            # Set the y-axis labels as the task labels
            ax.set_yticks(range(len(df.index)))
            ax.set_yticklabels(df['task_label'])

            # Set the y-axis limits
            ax.set_ylim(-0.5, len(df) - 0.5)

            # Set the x-axis limits based on the maximum value of days_start_to_end
            max_duration = df['days_start_to_end'].max()
            ax.set_xlim(0, max_duration)

            # Set the x-axis tick positions and labels
            ax.set_xticks(range(30))
            ax.set_xticklabels(range(30))

            # Assign different colors to each user
            users = df['display_name'].unique()
            user_colors = {'blue': 'User1', 'red': 'User2', 'green': 'User3', 'orange': 'User4', 'purple': 'User5'}
            user_color_mapping = {user: color for user, color in zip(users, user_colors)}

            # Create the Gantt chart with color differences based on users
            for row_index, row in df.iterrows():
                userid = row['display_name']
                color = user_color_mapping[userid]
                ax.barh(row_index, row['days_start_to_end'], left=row['start_num'], height=0.8, color=color)

            # Customize the chart appearance
            plt.xlabel('Day to complete')
            plt.ylabel('Tasks')
            plt.title('Gantt Chart')

            # Add a legend
            legend_labels = [f"{user}" for user in user_color_mapping.keys()]
            legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in user_color_mapping.values()]
            plt.legend(legend_handles, legend_labels, loc='upper right', bbox_to_anchor=(1, 1))

            # Invert the y-axis to display tasks from top to bottom
            plt.gca().invert_yaxis()

            # Save the chart to a BytesIO object
            image_stream = BytesIO()
            plt.savefig(image_stream, format='png')
            image_stream.seek(0)

            image_file = discord.File(image_stream, filename='gantt_chart.png')

            # Send the image file as an attachment using ctx.reply
            await ctx.reply(file=image_file)
        else:
            await ctx.reply("No valid tasks found for Gantt Chart.")
