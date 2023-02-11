from django.core.management import BaseCommand
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.utils import numerate_cats_tuple, fix_hash_char
from bot.password_generator import pwd_generator
from goals.models import GoalCategory, Goal
import environ
import logging

env = environ.Env()


class Command(BaseCommand):
    help = 'Start receiving messages from the Telegram servers'

    def __init__(self):
        super().__init__()
        self.tg_client = TgClient(env('TG_CLIENT_TOKEN'))
        self.category_set: list = []
        self.category_ids: list = []
        self.goal_set: list = []
        self.category_selection_state: bool = False
        self.selected_category: GoalCategory | None = None
        self.goal_title_state: bool = False
        self.logger = logging.getLogger(__name__)
        self.logger.info('Bot start polling')

    def handle(self, *args, **options) -> None:
        offset = 0
        self.logger.info('Waiting for messages from the bot\nPress Ctrl+C to interrupt')

        try:
            while True:
                res = self.tg_client.get_updates(offset=offset)
                for item in res.result:
                    if item.message:
                        self.logger.info(f'Message from telegram user {item.message.from_.username} - '
                                         f'{item.message.text}')
                        offset = item.update_id + 1
                        pwd = pwd_generator()
                        tg_user, created = TgUser.objects.get_or_create(
                            tg_chat_id=item.message.chat.id,
                            defaults={'tg_user_name': item.message.from_.username}
                        )

                        # tg_user writes to bot for the first time
                        if created:
                            self.tg_client.send_message(item.message.chat.id,
                                                        'Nice to meet you!.'
                                                        'Verify your account on '
                                                        'https://tick-tick.ml with this code please')
                            self.tg_client.send_message(item.message.chat.id, pwd)
                            tg_user.verification_code = pwd
                            tg_user.save()

                        # tg_user exists, but does not verify the code
                        elif not tg_user.user_id:
                            self.tg_client.send_message(item.message.chat.id,
                                                        'Amigo...😁\nTo continue using the service, '
                                                        'please confirm the verification code on '
                                                        'https://tick-tick.ml\n\n'
                                                        'Your code is ⬇')
                            self.tg_client.send_message(item.message.chat.id, pwd)
                            tg_user.verification_code = pwd
                            tg_user.save()

                        # /cancel entered
                        elif tg_user.user_id and item.message.text == '/cancel':
                            self.tg_client.send_message(item.message.chat.id,
                                                        'Operation cancelled.\n\n'
                                                        'Enter /goals to view all your goals.\n\n'
                                                        'Enter /create to create a new goal')
                            self.category_selection_state = False
                            self.goal_title_state = False

                        # '/goal' entered, displays list of user goals on boards, where he is owner or writer
                        elif tg_user.user_id and item.message.text == '/goals':
                            category_set = GoalCategory.objects.all().filter(
                                board__participants__user_id=tg_user.user_id,
                                is_deleted=False,
                                board__participants__role__in=[1, 2]
                            )
                            self.goal_set = list(Goal.objects.filter(
                                status__in=[1, 2, 3],
                                category__in=category_set
                            ).values_list('title', flat=True))

                            self.goal_set = fix_hash_char(self.goal_set)

                            self.tg_client.send_message(item.message.chat.id, 'List of your goals:\n\n' +
                                                        '\n'.join(self.goal_set))
                            self.logger.info('\n'.join(self.goal_set))

                        # '/create' entered, displays list of user categories on boards, where he is owner or writer
                        elif tg_user.user_id and item.message.text == '/create' \
                                and not self.category_selection_state and not self.goal_title_state:
                            self.category_set = list(
                                GoalCategory.objects.filter(board__participants__user_id=tg_user.user_id,
                                                            is_deleted=False,
                                                            board__participants__role__in=[1, 2]
                                                            ).values_list('id', 'title', ))

                            self.category_ids = [x[0] for x in self.category_set]
                            self.tg_client.send_message(item.message.chat.id,
                                                        'Click on the number to select a category: \n\n'
                                                        + numerate_cats_tuple(self.category_set))
                            self.logger.info(numerate_cats_tuple(self.category_set))
                            self.category_selection_state = True

                        # non-existing category entered
                        elif tg_user.user_id and self.category_selection_state and len(item.message.text) >= 2 \
                                and item.message.text[1:].isdigit() \
                                and int(item.message.text[1:]) not in self.category_ids:
                            self.tg_client.send_message(item.message.chat.id,
                                                        'Category doesn\'t exist\n'
                                                        'Enter an existing one or /cancel to cancel the operation')

                        # existing category entered
                        elif tg_user.user_id and self.category_selection_state and len(item.message.text) >= 2 \
                                and item.message.text[1:].isdigit() \
                                and int(item.message.text[1:]) in self.category_ids:
                            self.selected_category = GoalCategory.objects.get(id=int(item.message.text[1:]))
                            self.tg_client.send_message(item.message.chat.id,
                                                        'Great! Now enter goal title\n'
                                                        'or /cancel to cancel the operation')
                            self.goal_title_state = True

                        # category created
                        elif tg_user.user_id and self.category_selection_state \
                                and self.goal_title_state:
                            new_goal = Goal.objects.create(title=item.message.text,
                                                           user_id=tg_user.user_id,
                                                           category=self.selected_category)
                            category_set = GoalCategory.objects.filter(
                                board__participants__user_id=tg_user.user_id,
                                is_deleted=False,
                                board__participants__role__in=[1, 2]
                            )
                            self.goal_set = list(Goal.objects.filter(
                                status__in=[1, 2, 3],
                                category__in=category_set
                            ).values_list('title', flat=True))

                            new_goal.title = new_goal.title.replace('#', '%23')
                            self.goal_set = fix_hash_char(self.goal_set)
                            self.tg_client.send_message(item.message.chat.id,
                                                        f'Goal \'{new_goal.title}\' has been successfully created.\n\n'
                                                        'List of your goals:\n' +
                                                        '\n'.join(self.goal_set))
                            self.logger.info('\n'.join(self.goal_set))
                            self.category_selection_state = False
                            self.goal_title_state = False

                        # all other cases
                        else:
                            self.tg_client.send_message(item.message.chat.id,
                                                        'I don\'t understand you ¯\\_(ツ)_/¯\n\n'
                                                        'Enter /goals to view all your goals.\n\n'
                                                        'Enter /create to create a new goal.')
                            self.category_selection_state = False
                            self.goal_title_state = False
                            self.selected_category = None
                            self.category_set = []
                            self.category_ids = []
                            self.goal_set = []

        except KeyboardInterrupt:
            self.logger.info('\nPolling has finished')
