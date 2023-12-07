"""Test navigation to directory links"""


import os

from .utils import TREE_PAGE, EDITOR_PAGE
from jupyter_server.utils import url_path_join
pjoin = os.path.join


def url_in_tree(nb, url=None):
    """Ensure we're in the tree page somewhere (the file browser page)"""
    if url is None:
        url = nb.get_page_url(page=TREE_PAGE)

    tree_url = url_path_join(nb.get_server_info(), 'tree')
    return True if tree_url in url else False


def navigate_to_link(nb, item_text):
    print(f'[Test]   Now navigating to "{item_text}"')
    notebook_frontend = nb

    # Define a match finder func (this is easier
    # to hook into for debugging than a listcomp)
    def get_matches():
        print(f'[Test]     Attempt to find matches...')
        tree_page_items = [item for item in notebook_frontend.locate_all('#notebook_list .item_link', TREE_PAGE)]
        if tree_page_items:
            print(f'[Test]       Found!')
        return [elem for elem in tree_page_items if elem.is_visible() and elem.get_inner_text().strip() == item_text]
    # Get tree page item matching the item_text (the dir name/link element to navigate to)
    matches = notebook_frontend.wait_for_condition(
        lambda: get_matches(),
        period=3
    )
    target_element = matches[0]
    target_link = target_element.get_attribute("href")
    target_element.click()
    notebook_frontend.wait_for_condition(
        lambda: not notebook_frontend.locate(
            f'#notebook_list .item_link >> text="{item_text}"',
            page=EDITOR_PAGE).is_visible()
    )
    print(f'[Test]     Check URL in tree')
    notebook_frontend.wait_for_condition(
        lambda: url_in_tree(notebook_frontend),
        timeout=60,
        period=5
    )
    print(f'[Test]     Check URL matches link')
    print(f'[Test]       Item link: "{target_link}"')
    print(f'[Test]       Current URL is: "{notebook_frontend.get_page_url(page=TREE_PAGE)}"')
    notebook_frontend.wait_for_condition(
        lambda: target_link in notebook_frontend.get_page_url(page=TREE_PAGE),
        timeout=60,
        period=5
    )
    print(f'[Test]     Passed!')
    return notebook_frontend.get_page_url(page=TREE_PAGE)


def test_navigation(notebook_frontend):
    print('[Test] [test_dashboard_nav] Start! y2')

    # NOTE: The paths used here are currently define in
    # the server setup fixture (dirs/names are created there)
    # TODO: Refactor to define those dirs/names here

    SUBDIR1 = 'sub ∂ir1'
    SUBDIR2 = 'sub ∂ir2'
    SUBDIR1A = 'sub ∂ir 1a'
    SUBDIR1B = 'sub ∂ir 1b'

    # Start at the root (tree) URL
    print(f'[Test] Start at tree (root) URL')
    tree_url = notebook_frontend.get_page_url(page=TREE_PAGE)
    print(f'[Test]   URL is now at "{tree_url}"')

    # Test navigation to first folder from root
    print(f'[Test] Navigate to subdir1')
    subdir1_url = navigate_to_link(notebook_frontend, SUBDIR1)
    print(f'[Test]   URL is now at "{subdir1_url}"')

    # Test navigation to first subfolder (1a)
    print(f'[Test] Navigate to subdir1a')
    subdir1a_url = navigate_to_link(notebook_frontend, SUBDIR1A)
    print(f'[Test]   URL is now at "{subdir1a_url}"')
    notebook_frontend.go_back(page=TREE_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.get_page_url(page=TREE_PAGE) == subdir1_url,
        timeout=300,
        period=5
    )
    notebook_frontend.go_back(page=TREE_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.get_page_url(page=TREE_PAGE) == tree_url,
        timeout=300,
        period=5
    )
    # Wait for the links to update (subdir1a link should NOT be showing anymore)
    notebook_frontend.wait_for_condition(
        lambda: not notebook_frontend.locate(
            f'#notebook_list .item_link >> text="{SUBDIR1A}"',
            page=EDITOR_PAGE).is_visible()
    )

    # Test navigation to second folder from root
    print(f'[Test] Navigate to subdir2')
    subdir2_url = navigate_to_link(notebook_frontend, SUBDIR2)
    print(f'[Test]   URL is now at "{subdir2_url}"')
    # Wait for the links to update (subdir2 link should NOT be showing anymore)
    notebook_frontend.wait_for_condition(
        lambda: not notebook_frontend.locate(
            f'#notebook_list .item_link >> text="{SUBDIR2}"',
            page=EDITOR_PAGE).is_visible()
    )

    # Test navigation to second subfolder (1b)
    print(f'[Test] Navigate to subdir1b')
    subdir1b_url = navigate_to_link(notebook_frontend, SUBDIR1B)
    print(f'[Test]   URL is now at "{subdir1b_url}"')
    notebook_frontend.go_back(page=TREE_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.get_page_url(page=TREE_PAGE) == subdir2_url,
        timeout=300,
        period=5
    )
    notebook_frontend.go_back(page=TREE_PAGE)
    notebook_frontend.wait_for_condition(
        lambda: notebook_frontend.get_page_url(page=TREE_PAGE) == tree_url,
        timeout=300,
        period=5
    )

    print('[Test] [test_dashboard_nav] Finished!')
