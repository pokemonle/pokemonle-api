import { fetcher } from "../utils/axios";

export const GameInit = (gen: number, difficulty = 0) =>
  fetcher("/game/init", { gen, difficulty });

export const GameGuess = (answer: number, guess: string) =>
  fetcher("/game/guess", { answer, guess });
