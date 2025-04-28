import { useEffect, useState } from "react";
import { SearchBar } from "../compoents/SearchBar";
import { Button, addToast } from "@heroui/react";
import GameCard from "./GameCard";
import { GameInit, GameGuess } from "../api/game";
import { useEncodeGeneration } from "../hooks/useGeneration";

export const Game = () => {
  const [selectedPokemon, setSelectedPokemon] = useState<string | undefined>(
    undefined
  );
  const [answer, setAnswer] = useState<number | undefined>(undefined);
  const [isFinished, setFinished] = useState(false);
  const [compareList, setCompareList] = useState<Array<GameGuessData>>([]);

  const { data: encodeGeneration } = useEncodeGeneration();

  useEffect(() => {
    GameInit(encodeGeneration).then(setAnswer);
  }, [encodeGeneration]);

  const handleSearchChange = (value: string) => {
    setSelectedPokemon(value);
  };

  return (
    <>
      <div className="flex flex-col items-center m-4">
        <SearchBar value={selectedPokemon} onChange={handleSearchChange} />
        <div
          id="button-group"
          className="flex w-full mt-6 space-x-3 justify-center"
        >
          <Button
            color="primary"
            className="w-32"
            isDisabled={!selectedPokemon || isFinished}
            onPress={() => {
              if (answer && selectedPokemon) {
                GameGuess(answer, selectedPokemon ?? "").then((res) => {
                  console.log(res);
                  if (res.index === answer) {
                    setFinished(true);
                    addToast({
                      title: "恭喜你！",
                      description: "你猜对了！",
                      color: "success",
                      timeout: 2000,
                    });
                  }
                  setCompareList((prev) => [...prev, res]);
                });
              }
            }}
          >
            提交
          </Button>
          <Button color="danger" className="w-32">
            投降
          </Button>
          <Button
            color="success"
            onPress={() => {
              addToast({
                title: "恭喜你！",
                description: "你猜对了！",
                color: "success",
                timeout: 2000,
              });
            }}
            className="w-32"
          >
            重开
          </Button>
        </div>
        <div className="flex w-full mt-6 space-x-3 justify-center">
          <GameCard items={compareList} />
        </div>
      </div>
    </>
  );
};
