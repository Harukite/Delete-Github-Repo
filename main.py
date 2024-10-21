import requests
import os
import asyncio
from dotenv import load_dotenv
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.application import get_app

def get_github_repos(token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    repos = []
    page = 1
    while True:
        response = requests.get(
            f'https://api.github.com/user/repos?page={page}&per_page=100',
            headers=headers
        )
        if response.status_code == 200:
            page_repos = response.json()
            if not page_repos:
                break
            repos.extend(page_repos)
            page += 1
        else:
            print(f"获取仓库失败。状态码: {response.status_code}")
            return None
    return repos

async def delete_repo(token, username, repo):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.delete(f'https://api.github.com/repos/{username}/{repo}', headers=headers)
    await asyncio.sleep(1)  # 模拟删除过程
    if response.status_code == 204:
        return True
    else:
        return False

def create_repo_manager(repos, token, username):
    kb = KeyBindings()
    selected_index = [0]
    selected_repos = set()
    deleted_repos = []
    deleting_repos = set()

    def get_formatted_repos():
        lines = []
        for i, repo in enumerate(repos):
            prefix = '> ' if i == selected_index[0] else '  '
            if repo['name'] in deleting_repos:
                checkbox = '[D]'
            elif repo['name'] in selected_repos:
                checkbox = '[x]'
            else:
                checkbox = '[ ]'
            lines.append(f'{prefix}{checkbox} {repo["name"]}')
        return '\n'.join(lines)

    @kb.add('up')
    def _(event):
        selected_index[0] = (selected_index[0] - 1) % len(repos)
        event.app.invalidate()

    @kb.add('down')
    def _(event):
        selected_index[0] = (selected_index[0] + 1) % len(repos)
        event.app.invalidate()

    @kb.add('space')
    def _(event):
        if repos:
            repo_name = repos[selected_index[0]]['name']
            if repo_name in selected_repos:
                selected_repos.remove(repo_name)
            else:
                selected_repos.add(repo_name)
            event.app.invalidate()

    @kb.add('a')
    def _(event):
        selected_repos.update(repo['name'] for repo in repos)
        event.app.invalidate()

    @kb.add('i')
    def _(event):
        selected_repos.symmetric_difference_update(repo['name'] for repo in repos)
        event.app.invalidate()

    @kb.add('enter')
    async def _(event):
        repos_to_delete = list(selected_repos)
        for repo_name in repos_to_delete:
            deleting_repos.add(repo_name)
            event.app.invalidate()
            if await delete_repo(token, username, repo_name):
                deleted_repos.append(repo_name)
                selected_repos.remove(repo_name)
                repos[:] = [repo for repo in repos if repo['name'] != repo_name]
            deleting_repos.remove(repo_name)
            event.app.invalidate()
        selected_index[0] = min(selected_index[0], len(repos) - 1)
        # tasks = [delete_repo(token, username, repo_name) for repo_name in repos_to_delete]
        # results = await asyncio.gather(*tasks)
        # return [repo for repo, success in zip(repos_to_delete, results) if success]

    @kb.add('c-c')
    def _(event):
        event.app.exit()

    instructions = HSplit([
        Window(FormattedTextControl('使用方向键上下移动')),
        Window(FormattedTextControl('空格键选择/取消选择仓库')),
        Window(FormattedTextControl('a 键全选仓库')),
        Window(FormattedTextControl('i 键反选仓库')),
        Window(FormattedTextControl('回车键删除选中的仓库')),
        Window(FormattedTextControl('Ctrl+C 退出程序')),
        Window(FormattedTextControl('[ ] 未选择, [x] 已选择, [D] 正在删除')),
    ])

    repos_window = Window(FormattedTextControl(get_formatted_repos))

    root_container = HSplit([
        instructions,
        Window(height=1, char='-'),
        repos_window,
    ])

    layout = Layout(root_container)

    style = Style.from_dict({
        'window': 'bg:#000000 #ffffff',
    })

    application = Application(
        layout=layout,
        key_bindings=kb,
        style=style,
        full_screen=True,
    )

    asyncio.get_event_loop().run_until_complete(application.run_async())
    return deleted_repos

def main():
    load_dotenv()
    token = os.getenv('GITHUB_TOKEN')
    username = os.getenv('GITHUB_USERNAME')

    if not token or not username:
        print("请在 .env 文件中设置 GITHUB_TOKEN 和 GITHUB_USERNAME")
        return

    print("正在获取仓库列表...")
    repos = get_github_repos(token)
    if not repos:
        return

    deleted_repos = create_repo_manager(repos, token, username)

    if deleted_repos:
        print(f"\n已删除以下仓库：{', '.join(deleted_repos)}")
    else:
        print("\n没有删除任何仓库。")

if __name__ == "__main__":
    main()
