import { useEffect, useState } from "react";
import { SearchBar } from "../compoents/SearchBar";
import { Button } from "@heroui/react";
import { GameInit, GameGuess } from "../api/game";
import { useEncodeGeneration } from "../hooks/useGeneration";

export const Game = () => {
  const [selectedPokemon, setSelectedPokemon] = useState<string | undefined>(
    undefined
  );
  const [answer, setAnswer] = useState<number | undefined>(undefined);
  const { data: encodeGeneration } = useEncodeGeneration();

  useEffect(() => {
    GameInit(encodeGeneration).then(setAnswer);
  }, [encodeGeneration]);

  const handleSearchChange = (value: string) => {
    setSelectedPokemon(value);
  };

  return (
    <>
      <div className="flex flex-col items-center mt-4">
        <SearchBar value={selectedPokemon} onChange={handleSearchChange} />
        <div id="button-group" className="flex mt-6 space-x-3">
          {/* TODO */}
          <Button
            color="primary"
            className="w-32"
            onPress={() => {
              if (answer && selectedPokemon) {
                GameGuess(answer, selectedPokemon ?? "").then((res) => {
                  console.log(res);
                });
              }
            }}
          >
            提交
          </Button>
          <Button color="danger" className="w-32">
            投降
          </Button>
          <Button color="success" className="w-32">
            重开
          </Button>
        </div>
      </div>
    </>
  );
};
