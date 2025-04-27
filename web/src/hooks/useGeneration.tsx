import { useMemo } from "react";
import { useGenerationList } from "./useFetch";
import useSettings from "./useSettings";

export const useGenerationIDList = () => {
  const { data: generationList } = useGenerationList();
  const { settings } = useSettings();

  const generationIDs = useMemo(() => {
    return generationList
      ? generationList
          .filter((item) => settings.checkedValues.includes(item.identifier))
          .map((item) => item.id)
      : [];
  }, [generationList, settings.checkedValues]);

  return { data: generationIDs };
};

export const useEncodeGeneration = () => {
  const { settings } = useSettings();

  return { data: settings.encodeGeneration };
};
