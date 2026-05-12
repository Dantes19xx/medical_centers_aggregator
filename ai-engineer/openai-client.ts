import OpenAI from "openai";

let client: OpenAI | null = null;

export const OPENAI_MODEL = process.env.OPENAI_MODEL || "gpt-4o-mini";

export function getOpenAIClient(): OpenAI {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY is required");
  }

  if (!client) {
    client = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });
  }

  return client;
}
