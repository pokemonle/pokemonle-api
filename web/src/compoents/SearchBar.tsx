import { useState } from "react";
import { Autocomplete, AutocompleteItem } from "@heroui/react";
import { usePokemonName } from "../hooks/useFetch";

interface SerachBarProps {
  onChange?: (value: string) => void;
  value?: string;
}

export const SearchBar = (props: SerachBarProps) => {
  const { onChange } = props;

  const [search, setSearch] = useState("");
  const { data } = usePokemonName(search);

  return (
    <Autocomplete
      className="w-5/6 sm:max-w-md"
      items={data ?? []}
      label="Select a pokemon"
      placeholder="Type to search..."
      variant="bordered"
      value={props.value}
      onSelectionChange={(key) => {
        onChange?.(key?.toString() ?? "");
      }}
      onInputChange={(setValue) => {
        setSearch(setValue);
      }}
    >
      {(item) => (
        <AutocompleteItem key={item.pokemon_species_id} className="capitalize">
          {item.name}
        </AutocompleteItem>
      )}
    </Autocomplete>
  );
};
