from typing import Any

import pygame

from src.enums import StudyGroup
from src.gui.interface.dialog import DialogueManager
from src.screens.level import Level
from src.settings import GAME_LANGUAGE, SCREEN_HEIGHT, SCREEN_WIDTH, TB_SIZE
from src.sprites.entities.player import Player


class Tutorial:
    """Tutorial object.
    This class will be used to display the tutorial section to the player.
    Notice: after completing the tutorial and saving the game,
            it will not be displayed after relaunching the game."""

    def __init__(
        self,
        sprite_group: pygame.sprite.Group,
        player: Player,
        level: Level,
        round_config: dict[str, Any],
    ):
        self.dialogue_manager = DialogueManager(
            sprite_group, f"data/textboxes/{GAME_LANGUAGE}/tutorial.json"
        )
        self.player = player
        self.level = level
        self.round_config = round_config

        # position of the tutorial text box
        self.left_pos = SCREEN_WIDTH - TB_SIZE[0]
        self.top_pos = SCREEN_HEIGHT / 1.5 - TB_SIZE[1]
        # check if the player moved in the four directions
        self.movement_axis = [0, 0, 0, 0]

        self.instructions = {
            0: self.move,
            1: self.interact_with_ingroup_member,
            2: self.farm_tile,
            3: self.plant_crop,
            4: self.water_crop,
            5: self.go_to_forest_and_hit_tree,
            6: self.go_to_market_and_buy_sell_something,
            7: self.go_to_minigame_map_and_play,
            8: self.interact_with_outgroup_member,
            9: self.walk_around_outgroup_farm_and_switch_to_outgroup,
        }
        self.tasks_achieved = [False for _ in range(10)]
        self.current_task_index = 0

    # show instructions text boxes

    def farm_tile(self):
        self.dialogue_manager.open_dialogue("Farm_tile", self.left_pos, self.top_pos)

    def get_hat_ingroup(self):
        self.dialogue_manager.open_dialogue(
            "Get_hat_from_ingroup", self.left_pos, self.top_pos
        )

    def get_necklace_ingroup(self):
        self.dialogue_manager.open_dialogue(
            "Get_necklace_from_ingroup", self.left_pos, self.top_pos
        )

    def go_to_forest_and_hit_tree(self):
        self.dialogue_manager.open_dialogue(
            "Go_to_forest_and_hit_tree", self.left_pos, self.top_pos
        )

    def go_to_market_and_buy_sell_something(self):
        self.dialogue_manager.open_dialogue(
            "Go_to_market_and_buy/sell_something", self.left_pos, self.top_pos
        )

    def go_to_minigame_map_and_play(self):
        self.dialogue_manager.open_dialogue(
            "Go_to_minigame_map_and_play", self.left_pos, self.top_pos
        )

    def move(self):
        self.dialogue_manager.open_dialogue(
            "Basic_movement", self.left_pos, self.top_pos
        )

    def interact_with_ingroup_member(self):
        self.dialogue_manager.open_dialogue(
            "Interact_with_ingroup_member", self.left_pos, self.top_pos
        )

    def interact_with_outgroup_member(self):
        self.dialogue_manager.open_dialogue(
            "Interact_with_outgroup_member", self.left_pos, self.top_pos
        )

    def plant_crop(self):
        self.dialogue_manager.open_dialogue("Plant_crop", self.left_pos, self.top_pos)

    def walk_around_outgroup_farm_and_switch_to_outgroup(self):
        self.dialogue_manager.open_dialogue(
            "Walk_around_outgroup_farm_and_switch_to_outgroup",
            self.left_pos,
            self.top_pos,
        )

    def water_crop(self):
        self.dialogue_manager.open_dialogue("Water_crop", self.left_pos, self.top_pos)

    def show_tutorial_end(self):
        self.dialogue_manager.advance()
        self.dialogue_manager.open_dialogue("Tutorial_end", self.left_pos, self.top_pos)

    def switch_to_task(self, index: int):
        self.current_task_index = index
        if len(self.dialogue_manager._tb_list):
            self.dialogue_manager.advance()
            self.instructions[index]()
        else:
            self.instructions[index]()

    def check_tasks(self, game_paused):
        # first_not_done = next((i for i, j in enumerate(self.tasks_achieved) if j), None)
        for task_id, achieved in enumerate(self.tasks_achieved):

            if achieved:
                continue

            match task_id:
                case 0:
                    # check if the player achieved task "Basic movement"
                    if (
                        0 not in self.movement_axis
                        and self.dialogue_manager._get_current_tb().finished_advancing
                    ):
                        # TODO: fix this
                        self.tasks_achieved[task_id] = True
                        if self.current_task_index < task_id:
                            self.switch_to_task(task_id)
                    else:
                        self.current_task_index = task_id

                    if self.player.direction.x < 0:
                        self.movement_axis[0] = self.player.direction.x
                    elif self.player.direction.x > 0:
                        self.movement_axis[1] = self.player.direction.x
                    if self.player.direction.y < 0:
                        self.movement_axis[2] = self.player.direction.y
                    elif self.player.direction.y > 0:
                        self.movement_axis[3] = self.player.direction.y

                case 1:
                    # check if the player achieved task "interact with an ingroup member"
                    if (
                        self.dialogue_manager._get_current_tb().finished_advancing
                        and self.player.ingroup_member_interacted
                    ):
                        self.tasks_achieved[task_id] = True
                        if self.current_task_index < task_id:
                            self.switch_to_task(task_id)
                    else:
                        self.current_task_index = task_id

                case 2:
                    # check if the player achieved task "farm with your hoe"
                    if (
                        self.dialogue_manager._get_current_tb().finished_advancing
                        and self.level.tile_farmed
                    ):
                        self.tasks_achieved[task_id] = True
                        if self.current_task_index < task_id:
                            self.switch_to_task(task_id)
                    else:
                        self.current_task_index = task_id

                case 3:
                    # check if the player achieved task "plant a crop"
                    if (
                        True in self.level.crop_planted
                        and self.dialogue_manager._get_current_tb().finished_advancing
                    ):
                        self.switch_to_task(4)
                        self.tasks_achieved += 1

                case 4:
                    # check if the player achieved task "water the crop"
                    if (
                        self.level.crop_watered
                        and self.dialogue_manager._get_current_tb().finished_advancing
                    ):
                        self.switch_to_task(5)
                        self.tasks_achieved += 1

                case 5:
                    # check if the player achieved task "go to the forest and hit a tree"
                    if (
                        self.level.hit_tree
                        and self.dialogue_manager._get_current_tb().finished_advancing
                    ):
                        self.switch_to_task(6)
                        self.tasks_achieved += 1

                case 6:
                    # check if the player achieved task "go to the marketplace and buy or sell something"
                    if (
                        self.player.bought_sold
                        and not game_paused
                        and self.dialogue_manager._get_current_tb().finished_advancing
                    ):
                        self.switch_to_task(7)
                        self.tasks_achieved += 1

                case 7:
                    # check if the player achieved task "go to the minigame area and play "
                    if (
                        self.player.minigame_finished
                        and self.dialogue_manager._get_current_tb().finished_advancing
                    ):
                        self.switch_to_task(8)
                        self.tasks_achieved += 1

                case 8:
                    # check if the player achieved task "interact with an outgroup member"
                    if (
                        self.player.outgroup_member_interacted
                        and self.dialogue_manager._get_current_tb().finished_advancing
                    ):
                        if self.round_config.get("playable_outgroup", False):
                            self.switch_to_task(9)
                            self.tasks_achieved += 1

                            self.player.outgroup_member_interacted = False
                        else:
                            self.show_tutorial_end()
                            self.tasks_achieved = 10

                            self.player.blocked = True

                case 9:
                    # check if the player achieved task "walk around the outgroup farm and switch to the outgroup"
                    if (
                        self.player.study_group == StudyGroup.OUTGROUP
                        and self.dialogue_manager._get_current_tb().finished_advancing
                    ):
                        self.show_tutorial_end()
                        self.tasks_achieved += 1

                        self.player.blocked = True

                case 10:
                    # check if the player interacted to complete the tutorial
                    if (
                        self.dialogue_manager._get_current_tb().finished_advancing
                        and self.player.controls.INTERACT.hold
                    ):
                        self.player.blocked = False
                        self.dialogue_manager._purge_tb_list()
                        self.tasks_achieved += 1
                        self.level.player.save_file.is_tutorial_completed = True

    # run at the beginning of the tutorial
    def ready(self):
        if self.tasks_achieved == 0:
            self.switch_to_task(0)

    def update(self, game_paused):
        self.check_tasks(game_paused)
