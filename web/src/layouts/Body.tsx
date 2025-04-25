import { useState } from "react";
import { SearchBar } from "../compoents/SearchBar";
import { Button } from "@heroui/react";

export const Body = () => {
  const [selectedPokemon, setSelectedPokemon] = useState<string | undefined>(
    undefined
  );

  const handleSearchChange = (value: string) => {
    setSelectedPokemon(value);
    console.log("Selected Pokemon:", value);
  };
  return (
    <>
      <div className="flex flex-col items-center mt-4">
        <SearchBar value={selectedPokemon} onChange={handleSearchChange} />
        <div id="button-group" className="flex mt-6 space-x-2">
          {/* TODO */}
          <Button color="primary" className="w-32">
            随机
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
