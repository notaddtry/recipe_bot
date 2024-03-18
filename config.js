import dotenv from "dotenv";
dotenv.config();

export const TOKEN = process.env.TELEGRAM_TOKEN || "YOUR_TELEGRAM_BOT_TOKEN";
