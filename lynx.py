

"""
Finance tracker bot

/funds

List of remaining budget:

Food: {food_spending}/{food_budget}
Entertainment: {entertainment_spending}/{entertainment_budget}
Transport: {transport_spending}/{transport_budget}

###


/spent

inlinekeyboard:
option: Food | Entertainment | Transport

"How much did you spend on {selected_option}? "
*submit*
option_remaining = option_budget - option_spending
"Remaining for {selected_option} is {}"

/price

inlinekeyboard:
option: Food | Entertainment | Transport

"How much is it? "
eg. 100
option_remaining = option_budget - option_spending
if percentage < 20%:
    "You sure? This is percentage}% of your {option_remaining}. "
"This is percentage}% of your {option_remaining}."
"""


import logging
import csv

from telegram import (
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)

TOKEN = "5851573424:AAHyPE5j7ptfeuhooj-blckuuXcYUbBCg7I"


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["/spent", "/price", "/fund"]]

    await update.message.reply_text(
        "Hi! I'm the Pouncing Lynx! \n ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Select an option"
        ),
    )


"""
/funds

List of remaining budget:

Food: {food_spending}/{food_budget}
Entertainment: {entertainment_spending}/{entertainment_budget}
Transport: {transport_spending}/{transport_budget}
"""


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask user for which fund to """
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Thank you! I hope we can talk again some day.")

    return ConversationHandler.END



async def funds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show the balance of the funds"""
    user = update.message.from_user
    logger.info("Date of request from %s: %s", user.first_name, update.message.text)
    
    await update.message.reply_text(f"{show_budget(get_amounts())}")

    return ConversationHandler.END    

def get_amounts() -> list:
    """
    return amounts appended from budget.csv.
    """
    amounts = []
    with open("budget.csv") as budget:
        budget_reader = csv.DictReader(budget)
        for row in budget_reader:
            amounts.append({"Budget Name": row["budget_name"], "Budget": row["budget"]})
    return amounts

def show_budget(amounts):
    """
    Using list from get_amounts to return the list of budgets.
    """
    return (f'Budgets \n\n'
        f'{amounts[0]["Budget Name"]}: ${amounts[0]["Budget"]}\n'
        f'{amounts[1]["Budget Name"]}: ${amounts[1]["Budget"]}\n'
        f'{amounts[2]["Budget Name"]}: ${amounts[2]["Budget"]}')



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("funds", funds))
    # application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()