# select budget_name
# Provide budget
# retrieve the amount
# new amount = budget - amount
# append new amount to csv
# run check_amount()
# print(budget_name: budget)


AMOUNT = range(1)

async def spend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Ask for Employee ID and parse to add_register for checking
    """
    await update.message.reply_text("How much was it? ")

    return AMOUNT


async def spend_wallet_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    user = update.message.from_user
    logger.info("Option of %s: %s", user.first_name, update.message.text)
    spending = update.message.text

    keyboard = [
        [
            InlineKeyboardButton("Food", callback_data="Food"),
            InlineKeyboardButton("Entertainment", callback_data="Entertainment"),
        ],
        [InlineKeyboardButton("Transport", callback_data="Transport")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose a wallet:", reply_markup=reply_markup)

    return spending

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    get_amounts()


    await query.edit_message_text(text=f"Budget: \n\n{query.data}: ${show_budget(query.data)}")
        
    # await query.edit_message_text(text=f"Selected option: {query.data}")


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

def update_amount(spending, wallets, option):
    for wallet in wallets:
        if option == wallet["Budget Name"]:
            budget = int(wallet["Budget"])
            new_amount = budget - int(spending)
            return new_amount


def main():
    # Add Conversation Handler with states ADD_REGISTER
    spend_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("spend", spend)],
        states={
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, spend_wallet_options)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )