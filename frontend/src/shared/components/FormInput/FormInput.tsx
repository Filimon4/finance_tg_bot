import FormElementContainer from "../containers/FormElementContainer/FormElementContainer";

const FormInput = ({
  value,
  setValue,
  placeholder,
}: {
  value: string;
  setValue: React.Dispatch<React.SetStateAction<string | undefined>>;
  placeholder: string;
}) => {
  return (
    <FormElementContainer>
      <input
        className="outline-0 w-full h-full text-black p-5"
        placeholder={placeholder}
        value={value}
        onChange={(e) => setValue(e.currentTarget.value)}
        type="text"
      />
    </FormElementContainer>
  );
};

export default FormInput;
