import { useState } from "react";
import { Autocomplete, AutocompleteItem, Button } from "@heroui/react";
import { usePokemonName, usePokemonIDByGeneration } from "../hooks/useFetch";
import { useGenerationIDList } from "../hooks/useGeneration";

interface SerachBarProps {
  onChange?: (value: string) => void;
  value?: string;
}

export const SearchBar = (props: SerachBarProps) => {
  const { onChange } = props;

  const [search, setSearch] = useState("");

  const { data: generationIDs } = useGenerationIDList();

  const { data } = usePokemonName(generationIDs, search);
  const { data: PokemonIDs } = usePokemonIDByGeneration(generationIDs);

  const handleRandomPick = () => {
    if (PokemonIDs && PokemonIDs.length > 0) {
      const randomIndex = Math.floor(Math.random() * PokemonIDs.length);
      const randomPokemon = PokemonIDs[randomIndex];
      onChange?.(randomPokemon.toString());
    }
  };

  return (
    <div className="flex w-full items-center justify-center">
      <Autocomplete
        className="flex-1 sm:max-w-md"
        items={data ?? []}
        label="Select a pokemon"
        placeholder="Type to search..."
        variant="bordered"
        selectedKey={props.value}
        onSelectionChange={(key) => {
          onChange?.(key?.toString() ?? "");
        }}
        onInputChange={(setValue) => {
          setSearch(setValue);
        }}
      >
        {(item) => (
          <AutocompleteItem
            key={item.pokemon_species_id}
            className="capitalize"
          >
            {item.name}
          </AutocompleteItem>
        )}
      </Autocomplete>
      <Button
        onPress={handleRandomPick}
        color="secondary"
        size="lg"
        className="ml-2 w-24"
      >
        随机
      </Button>
    </div>
  );
};
