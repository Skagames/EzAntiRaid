"""
This file automatically detects when a user should be banned as part of a raid
"""
# TODO: Add feauture to turn off autoraid
# TODO: autoraid should ban the backlog as well
import time

class raidChecker():
    """
    
    """
    def __init__(self, member) -> None:
        """
        
        """
        # set the member and the guild attributes
        self.member = member
        self.guild = member.guild

        # boolean to check if the sync method has ran
        self.has_synced = False

        # sorted members list
        self.sorted_members = None


    async def sync(self) -> None:
        # get a list of all members in the server
        all_members = self.guild.members

        # make the list a readable and modifyable list.
        all_members_readable = [{'id': member.id, 'name': f"{member.name}#{member.discriminator}", 'joined_at': member.joined_at.timestamp()} for member in all_members]

        # sort the list according to join time
        all_members_readable_sorted = sorted(all_members_readable, key= lambda k: int(k['joined_at']))

        # save the list
        self.sorted_members = all_members_readable_sorted

    async def get_timespan_absolute(self, begin_time: int, end_time: int) -> list:
        if self.sorted_members is None:
            await self.sync
        
        return [member for member in self.sorted_members if begin_time < member['joined_at'] < end_time]


    async def get_timespan_relative(self, seconds_in_past):
        if self.sorted_members is None:
            await self.sync

        end_time = time.time()
        begin_time = end_time - seconds_in_past
        return [member for member in self.sorted_members if begin_time < member['joined_at'] < end_time]
    

    async def raidcheck(self):
        """
        main raid check function
        average joins per 3 minutes =>
        180 / (total_time_between_first_and_last_join / total_amount_of_users)
        """
        # get the average join rate of the server in users / 180 seconds
        sorted_members = await self.get_timespan_absolute(time.time() - 7890000, time.time() - 180) # we get the average of the past 3 months
        firstjoin, lastjoin = sorted_members[0]['joined_at'], sorted_members[-1]['joined_at']
        delta = lastjoin - firstjoin
        total_users = len(sorted_members)
        self.average_users = 180 / (delta / total_users)
        
        # get the average join rate of the past 3 minutes
        sorted_members = await self.get_timespan_relative(180) # get the last 3 minutes
        firstjoin, lastjoin = sorted_members[0]['joined_at'], sorted_members[-1]['joined_at']
        delta = lastjoin - firstjoin
        total_users = len(sorted_members)
        self.average_users_last_3_minutes = 180 / (delta / total_users)

        """
        The main problem occurs when the average join rate in the past 3 minutes is significantly higher
        than over the past 3 months.
        In this case we know a raid is occurring and the user should be banned
        The current cap is if the join rate is 25 times higher than the average. In this case
        we will ban the user.

        a safety net is in place for users that join after f.ex. a big announcement was made that
        gets a bigger influx of users in a moment, if the join factor is smaller
        than 25, but bigger than 12.5, the user will be kicked from the server

        on low join servers the average join rate could be so low that one join already sets of the
        alarm, for this we put a second safety net in place that the average join in the past 3 minutes
        needs to be more than 5 (Meaning that backpropagation needs to be in place)
        """

        # check if the join over past 3 minutes exceeds the treshold
        if self.average_users_last_3_minutes > 25 * self.average_users and self.average_users_last_3_minutes > 5:  # 20 being the threshold
            # ban the user himself
            await self.member.ban(delete_message_days=7, reason="Banned by EzAntiRaid (automatic)")
        elif self.average_users_last_3_minutes > 12.5 * self.average_users and self.average_users_last_3_minutes > 5:
            await self.member.kick(reason='Kicked by EzAntiRaid (automatic)')