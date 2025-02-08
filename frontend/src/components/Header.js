import { Box, Heading, Text, Image } from '@chakra-ui/react';

export default function Header() {
  return (
    <Box textAlign="center" mb={8}>
      <Image src="/logo.jpeg" alt="Syllabridge Logo" boxSize="100px" mx="auto" mb={4} />
      <Heading as="h1" size="2xl" fontWeight="bold" color="blue.900">
        Syllabridge
      </Heading>
      <Text fontSize="xl" color="gray.600">
        Upload your syllabus and get personalized learning resources
      </Text>
    </Box>
  );
}
