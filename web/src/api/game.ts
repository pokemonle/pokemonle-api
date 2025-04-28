import { fetcher } from "../utils/axios";

export const GameInit = (gen: number, difficulty = 0) =>
  fetcher<number>("/game/init", { gen, difficulty });

export const GameGuess = (answer: number, guess: string) =>
  fetcher<GameGuessData>("/game/guess", { answer, guess });
