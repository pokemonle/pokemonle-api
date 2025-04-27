import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  CheckboxGroup,
  Checkbox,
  RadioGroup,
  Radio,
  useDisclosure,
  Switch,
  Slider,
} from "@heroui/react";
import { useEffect } from "react";
import { useGenerationList } from "../hooks/useFetch";
import useSettings from "../hooks/useSettings";

export const SettingModal = () => {
  const { settings, setSettingKey } = useSettings();

  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const { data: generationList, mutate } = useGenerationList();

  if (generationList && settings.checkedValues.length === 0) {
    setSettingKey(
      "checkedValues",
      generationList.map((item) => item.identifier)
    );
  }

  // open modal lifecycle
  useEffect(() => {
    if (isOpen) {
      mutate();
    }
  }, [mutate, isOpen]);

  return (
    <>
      <Button size="sm" onPress={onOpen}>
        Settings
      </Button>
      <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                Modal Title
              </ModalHeader>
              <ModalBody>
                <RadioGroup isDisabled orientation="horizontal">
                  {["easy", "normal", "hard"].map((item, index) => (
                    <Radio value={item} key={index}>
                      {item}
                    </Radio>
                  ))}
                </RadioGroup>
                <div className="w-full border-t border-gray-300 my-1/2" />
                <CheckboxGroup
                  orientation="horizontal"
                  value={settings.checkedValues}
                  onValueChange={(newValues) => {
                    if (newValues.length > 0) {
                      setSettingKey("checkedValues", newValues);
                    }
                  }}
                >
                  {generationList
                    ? generationList.map((item) => (
                        <Checkbox
                          key={item.id}
                          value={item.identifier}
                          className="capitalize"
                          onChange={() => {
                            const newValue =
                              settings.encodeGeneration ^ (1 << (item.id - 1));
                            if (newValue !== 0) {
                              setSettingKey("encodeGeneration", newValue);
                            }
                          }}
                        >
                          {item.name}
                        </Checkbox>
                      ))
                    : []}
                </CheckboxGroup>
                <div className="w-full border-t border-gray-300 my-1/2" />
                <p className="font-bold">显示信息</p>
                <div className="flex flex-col gap-2">
                  <Switch
                    size="sm"
                    isSelected={settings.stats}
                    onValueChange={(val) => {
                      setSettingKey("stats", val);
                    }}
                  >
                    更多种族值信息
                  </Switch>
                  <Switch
                    size="sm"
                    isSelected={settings.shape}
                    onValueChange={(val) => {
                      setSettingKey("shape", val);
                    }}
                  >
                    更多外形信息
                  </Switch>
                  <Switch
                    size="sm"
                    isSelected={settings.eggGroup}
                    onValueChange={(val) => {
                      setSettingKey("eggGroup", val);
                    }}
                  >
                    蛋组/捕获率
                  </Switch>
                </div>
                <div className="w-full border-t border-gray-300 my-1/2" />
                <p className="font-bold">猜测次数: {settings.chance}</p>
                <Slider
                  value={settings.chance}
                  aria-label="Chance"
                  onChange={(val) => {
                    // value must be number
                    setSettingKey("chance", val as number);
                  }}
                  minValue={1}
                  maxValue={25}
                />
              </ModalBody>
              <ModalFooter>
                <Button color="danger" variant="light" onPress={onClose}>
                  Close
                </Button>
                <Button color="primary" onPress={onClose}>
                  Action
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
};
