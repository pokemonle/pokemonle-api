import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Chip,
  User,
} from "@heroui/react";
import { Key, useCallback } from "react";

interface GameCardProps {
  items: Array<GameGuessData>;
}

const columns = [
  { key: "index", label: "宝可梦" },
  { key: "type", label: "属性" },
  { key: "gen", label: "Generation" },
  { key: "ability", label: "Ability" },
  { key: "stat", label: "Stats" },
];

const UpArrow = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={2}
    stroke="currentColor"
    className="w-4 h-4"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M5 10l7-7m0 0l7 7m-7-7v18"
    />
  </svg>
);

const DownArrow = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={2}
    stroke="currentColor"
    className="w-4 h-4"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M19 14l-7 7m0 0l-7-7m7 7V3"
    />
  </svg>
);

const CheckIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={2}
    stroke="currentColor"
    className="w-4 h-4"
  >
    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
  </svg>
);

const GameCard = (props: GameCardProps) => {
  const renderCell = useCallback((item: GameGuessData, key: Key) => {
    const value = item[key as keyof GameGuessData];

    switch (key) {
      case "index":
        return (
          <User
            name={item.name}
            avatarProps={{
              radius: "lg",
              size: "lg",
              src: `https://pokeimg.oss-cn-beijing.aliyuncs.com/pokemon_images/${item.index}.webp`,
            }}
          >
            {item.name}
          </User>
        );
      case "type":
        return (
          <div className="flex flex-col space-y-1">
            {item.type.map((type, index) => {
              return (
                <Chip
                  key={`${item.index}-${index}`}
                  variant="flat"
                  color={type.value ? "success" : "default"}
                  className="flex justify-center items-center"
                >
                  <p className="w-16 truncate text-center">{type.key}</p>
                </Chip>
              );
            })}
          </div>
        );

      case "ability":
        return (
          <div className="flex flex-col space-y-1">
            {item.ability.map((a, index) => {
              return (
                <Chip
                  key={`${item.index}-${index}`}
                  variant="flat"
                  color={a.value ? "success" : "default"}
                  className="flex justify-center items-center"
                >
                  <p className="w-16 truncate text-center">{a.key}</p>
                </Chip>
              );
            })}
          </div>
        );
      case "gen":
        return (
          <Chip
            variant="flat"
            color={item.gen.value === "equiv" ? "success" : "default"}
          >
            <div className="flex items-center space-x-2">
              <p>{item.gen.key}</p>
              {item.gen.value !== "equiv" ? (
                <>{item.gen.value === "high" ? <UpArrow /> : <DownArrow />}</>
              ) : (
                <CheckIcon />
              )}
            </div>
          </Chip>
        );
      case "stat":
        return (
          <Chip
            variant="flat"
            color={item.stat.pow.value === "equiv" ? "success" : "default"}
          >
            <div className="flex items-center space-x-2">
              <p>{item.stat.pow.key}</p>
              {item.stat.pow.value !== "equiv" ? (
                <>
                  {item.stat.pow.value === "high" ? <UpArrow /> : <DownArrow />}
                </>
              ) : (
                <CheckIcon />
              )}
            </div>
          </Chip>
        );
      default:
        return value as number;
    }
  }, []);

  return (
    <>
      <Table aria-label="pokemon compare table">
        <TableHeader columns={columns}>
          {(column) => (
            <TableColumn key={column.key} className="capitalize">
              {column.label}
            </TableColumn>
          )}
        </TableHeader>
        <TableBody items={props.items}>
          {(item) => (
            <TableRow key={item.index}>
              {(columnKey) => (
                <TableCell>{renderCell(item, columnKey)}</TableCell>
              )}
            </TableRow>
          )}
        </TableBody>
      </Table>
    </>
  );
};

export default GameCard;
