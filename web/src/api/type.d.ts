interface GameGuessItemResult<T> {
  key: T;
  value: boolean;
}

interface GameGuessDistanceResult {
  key: number;
  value: "equiv" | "high" | "low";
  dis: "equiv" | "far" | "near";
}

interface GameGuessData {
  index: number;
  name: string;
  type: Array<GameGuessItemResult<string>>;
  ability: Array<GameGuessItemResult<string>>;
  gen: GameGuessDistanceResult;
  stat: {
    pow: GameGuessDistanceResult;
  };
}
