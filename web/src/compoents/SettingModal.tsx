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
} from "@heroui/react";
import { useEffect, useState } from "react";
import { useGenerations } from "../hooks/useFetch";

export const SettingModal = () => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const { data: generationList, mutate, isLoading } = useGenerations();
  const [checkedValues, setCheckedValues] = useState<string[]>([]);

  const [encodeGeneration, setEncodeGeneration] = useState<number>(511);

  useEffect(() => {
    if (generationList) {
      setCheckedValues(generationList.map((item) => item.identifier));
    }
  }, [isLoading, generationList]);

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
                {encodeGeneration}
                <RadioGroup orientation="horizontal">
                  {["easy", "normal", "hard"].map((item, index) => (
                    <Radio value={item} key={index}>
                      {item}
                    </Radio>
                  ))}
                </RadioGroup>

                <CheckboxGroup
                  orientation="horizontal"
                  value={checkedValues}
                  onValueChange={(newValues) => {
                    if (newValues.length > 0) {
                      setCheckedValues(newValues);
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
                              encodeGeneration ^ (1 << (item.id - 1));
                            if (newValue !== 0) {
                              setEncodeGeneration(newValue);
                            }
                          }}
                        >
                          {item.name}
                        </Checkbox>
                      ))
                    : []}
                </CheckboxGroup>
                {/* TODO */}
                <p>
                  Magna exercitation reprehenderit magna aute tempor cupidatat
                  consequat elit dolor adipisicing. Mollit dolor eiusmod sunt ex
                  incididunt cillum quis. Velit duis sit officia eiusmod Lorem
                  aliqua enim laboris do dolor eiusmod. Et mollit incididunt
                  nisi consectetur esse laborum eiusmod pariatur proident Lorem
                  eiusmod et. Culpa deserunt nostrud ad veniam.
                </p>
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
