import { useLocalStorage } from "usehooks-ts";

interface Settings {
  encodeGeneration: number;
  checkedValues: string[];
  difficulty: string;
  chance: number;
  stats: boolean;
  shape: boolean;
  eggGroup: boolean;
}

const useSettings = () => {
  const [settings, setSettings, removeSettings] = useLocalStorage<Settings>(
    "settings",
    {
      encodeGeneration: 511,
      checkedValues: [],
      difficulty: "normal",
      chance: 10,
      stats: true,
      shape: true,
      eggGroup: true,
    }
  );

  const setSettingKey = <K extends keyof Settings>(
    key: K,
    value: Settings[K]
  ) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
  };

  return {
    settings,
    setSettingKey,
    removeSettings,
  };
};

export default useSettings;
