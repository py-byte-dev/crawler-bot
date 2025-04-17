from decimal import Decimal


def main_menu_text(user_name: str) -> str:
    return f'Hello, {user_name}! 👋\n\nTo get started, please click the button below 👇'


def get_file_menu_text() -> str:
    return '📥 Upload your .xlsx file with resources data.'


def processed_resource_text(title: str, url: str, xpath: str, averege_price: Decimal) -> str:
    return (
        '✅ Success processed resource\n\n'
        f'◉ Title: {title}\n'
        f'◉ URL: {url}\n'
        f'◉ XPath: <code>{xpath}</code>\n'
        f'◉ Averege price: {averege_price}\n\n'
    )


def start_process_text() -> str:
    return '⚙️ Start processing resource...'


def error_text(details: str) -> str:
    return f'⚠️ <b>Error while processing your resource. Please try again.</b>\n\n<code>Details: {details}</code>'
