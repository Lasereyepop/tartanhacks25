import { Button as ChakraButton } from '@chakra-ui/react';

export default function Button({ text, onClick }) {
  return <ChakraButton w="full" colorScheme="blue" size="lg" onClick={onClick}>{text}</ChakraButton>;
}