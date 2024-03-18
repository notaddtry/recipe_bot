import TelegramBot from "node-telegram-bot-api";
import { TOKEN } from "../config.js";

const bot = new TelegramBot(TOKEN, { polling: true });

export const startBot = () => {
  bot.setMyCommands([
    { command: "/start", description: "Начать работу с ботом" },
    { command: "/get_recipe", description: "Получить рецепт" },
    { command: "/get_recipe_of_a_day", description: "Получить рецепт дня" },
    { command: "/katya_love", description: "Получить любовь" },
  ]);

  bot.on("message", async (msg) => {
    const chatId = msg.chat.id;
    const text = msg.text;

    if (text === "/start" || text === "/start@notaddtry_recipe_bot") {
      return bot.sendMessage(chatId, "Я тебя слушаю");
    }

    if (text === "/get_recipe" || text === "/get_recipe@notaddtry_recipe_bot") {
      return bot.sendMessage(chatId, "Находится в разработке");
    }

    if (
      text === "/get_recipe_of_a_day" ||
      text === "/get_recipe_of_a_day@notaddtry_recipe_bot"
    ) {
      return bot.sendMessage(chatId, "Находится в разработке");
    }

    if (text === "/katya_love" || text === "/katya_love@notaddtry_recipe_bot") {
      await bot.sendSticker(chatId, "./assets/photo_2020-11-27_23-31-06.webp");
      return bot.sendMessage(chatId, `${msg.from.first_name}, я тебя люблю`);
    }
  });
};
