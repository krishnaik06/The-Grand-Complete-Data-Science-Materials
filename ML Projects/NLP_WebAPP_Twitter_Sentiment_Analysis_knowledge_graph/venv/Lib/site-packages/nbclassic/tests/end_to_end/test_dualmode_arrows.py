"""Tests arrow keys on both command and edit mode"""
import time

from .utils import EDITOR_PAGE, EndToEndTimeout


INITIAL_CELLS = ['AAA', 'BBB', 'CCC']
JS_HAS_SELECTED = "(element) => { return element.classList.contains('selected'); }"


def test_dualmode_arrows(prefill_notebook):
    # Tests functionality related to up/down arrows and
    # the "j"/"k" shortcuts for up and down, in command
    # mode and in edit mode

    print('[Test] [test_dualmode_arrows] Start!')
    notebook_frontend = prefill_notebook(INITIAL_CELLS)

    # Make sure the top cell is selected
    print('[Test] Ensure top cell is selected')
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[0].evaluate(JS_HAS_SELECTED) is True
    )
    notebook_frontend.to_command_mode()

    # Move down (shortcut j) to the second cell and check that it's selected
    print('[Test] Move down ("j") to second cell')
    notebook_frontend.press("j", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[1].evaluate(JS_HAS_SELECTED) is True
    )

    # Move down to the third cell and check that it's selected
    print('[Test] Move down to third cell')
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[2].evaluate(JS_HAS_SELECTED) is True
    )

    # Move back up (shortcut k) to the second cell
    print('[Test] Move back up ("k") to second cell')
    notebook_frontend.press("k", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[1].evaluate(JS_HAS_SELECTED) is True
    )

    # Move up to the top cell
    print('[Test] Move to top')
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[0].evaluate(JS_HAS_SELECTED) is True
    )

    # Move up while already on the top cell and ensure it stays selected
    print('[Test] Move up while already on top')
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[0].evaluate(JS_HAS_SELECTED) is True
    )

    # Move down to the last cell + press down to ensure it's still selected
    print('[Test] Move to bottom and press down')
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[1].evaluate(JS_HAS_SELECTED) is True
    )
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[2].evaluate(JS_HAS_SELECTED) is True
    )
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[2].evaluate(JS_HAS_SELECTED) is True
    )

    # EDIT MODE TESTS

    # Delete all the cells, then add new ones to test
    # arrow key behaviors in edit mode on empty cells
    print('[Test] Prep cells for edit mode tests')
    [notebook_frontend.locate(".fa-cut.fa", page=EDITOR_PAGE).click() for i in range(4)]
    [notebook_frontend.press("b", page=EDITOR_PAGE) for i in range(2)]
    # Add a cell above, which will leave us selected
    # on the third cell out of 4 empty cells
    notebook_frontend.press("a", page=EDITOR_PAGE)

    # Start editing the third empty cell
    print('[Test] Enter edit mode on the third cell')
    notebook_frontend.press("Enter", page=EDITOR_PAGE)
    # Check that the cell is being edited
    notebook_frontend.wait_for_selector('.CodeMirror-focused', page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[2].locate('.CodeMirror-focused')
    )

    # Arrow up in edit mode on this empty cell (should move to edit move
    # on the cell above when a cell is empty)
    print('[Test] Arrow up in edit mode to the second cell')
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[1].evaluate(JS_HAS_SELECTED) is True
    )
    # Type a 1 in edit mode, then arrow left (to the beginning of the cell)
    # and then up, which should then move to edit mode in the cell above
    print('[Test] Enter a "1" in the second cell')
    notebook_frontend.press("1", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowLeft", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[0].evaluate(JS_HAS_SELECTED) is True,
    )
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.get_cells_contents() == ['', '1', '', ''],
    )

    print('[Test] Move to the top cell and edit')
    # Arrow up again while on the top cell, it should still be selected
    notebook_frontend.press("ArrowUp", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[0].evaluate(JS_HAS_SELECTED) is True
    )
    # Enter a 0 in the top cell (we're still in edit mode)
    print('[Test] Enter a "0" in the top cell')
    notebook_frontend.press("0", page=EDITOR_PAGE)

    # Move down, right, down, while the edit mode cursor is on the top cell,
    # after the 0 char...this should move down a cell (to the second cell),
    # then right to the end of the 1 char in the second cell, then down to
    # the third empty cell
    print('[Test] Move down to the third cell and edit')
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowRight", page=EDITOR_PAGE)
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    # Put a 2 in the third cell
    print('[Test] Enter a "2" in the third cell')
    notebook_frontend.press("2", page=EDITOR_PAGE)

    # Move down to the last cell, then down again while on the bottom cell
    # (which should stay in the bottom cell), then enter a 3 in the bottom
    # (fourth) cell
    print('[Test] Move down to the bottom cell and edit')
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[3].evaluate(JS_HAS_SELECTED) is True
    )
    notebook_frontend.press("ArrowDown", page=EDITOR_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.cells[3].evaluate(JS_HAS_SELECTED) is True
    )
    notebook_frontend.wait_for_condition(  # Ensure it's in edit mode
        lambda: notebook_frontend.cells[3].locate('.CodeMirror-focused'),
    )  # If it's not located, the FrontendElement will be Falsy
    print('[Test] Enter a "3" in the fourth cell')
    notebook_frontend.press("3", page=EDITOR_PAGE)
    notebook_frontend.to_command_mode()
    print('[Test] Check the results match expectations')
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.get_cells_contents() == ["0", "1", "2", "3"]
    )
