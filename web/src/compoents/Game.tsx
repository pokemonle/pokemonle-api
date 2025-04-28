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
  const [restartCount, setRestartCount] = useState(0);

  const { data: encodeGeneration } = useEncodeGeneration();

  useEffect(() => {
    GameInit(encodeGeneration).then(setAnswer);
  }, [encodeGeneration, restartCount]);

  const handleSearchChange = (value: string) => {
    setSelectedPokemon(value);
  };

  const handleRestart = () => {
    setFinished(false);
    setCompareList([]);
    setSelectedPokemon(undefined);
    setAnswer(undefined);

    setRestartCount((prev) => prev + 1);
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
                const selectIndex: number = parseInt(selectedPokemon);
                GameGuess(answer, selectIndex).then((res) => {
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
          <Button
            isDisabled={isFinished}
            color="danger"
            className="w-32"
            onPress={() => {
              if (answer) {
                GameGuess(answer, answer).then((res) => {
                  console.log(res);
                  if (res.index === answer) {
                    setFinished(true);
                    addToast({
                      title: "已投降！",
                      description: "胜败乃兵家常事,请重新来过！",
                      color: "warning",
                      timeout: 2000,
                    });
                  }
                  setCompareList((prev) => [...prev, res]);
                });
              }
            }}
          >
            投降
          </Button>
          <Button color="success" onPress={handleRestart} className="w-32">
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
