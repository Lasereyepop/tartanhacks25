import { useState } from 'react';
import { Box, Input, Select, VStack, Grid, Text, Flex, Button as ChakraButton } from '@chakra-ui/react';
import Button from './Button';
import Results from './Results';

export default function Form({ setResults }) {
  const [institution, setInstitution] = useState('');
  const [major, setMajor] = useState('');
  const [courseNumber, setCourseNumber] = useState('');
  const [courseName, setCourseName] = useState('');
  const [futureCareer, setFutureCareer] = useState('');
  const [syllabusFile, setSyllabusFile] = useState(null);
  const [syllabusUrl, setSyllabusUrl] = useState('');
  const [resultsData, setResultsData] = useState(null);

  const handleSubmit = async () => {
    const formData = new FormData();
    if (syllabusFile) {
      formData.append("file", syllabusFile);
    } else if (syllabusUrl) {
      formData.append("url", syllabusUrl);
    }

    try {
      const response = await fetch("http://localhost:8000/upload-pdf", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload syllabus");
      }

      const result = await response.json();
      setResults(result);
      setResultsData(result);
    } catch (error) {
      console.error("Error uploading syllabus:", error);
    }
  };

  return (
    <VStack spacing={6} bg="white" p={8} borderRadius="lg" boxShadow="lg" width="full" maxW="800px" mx="auto">
      {resultsData ? (
        <Results data={resultsData} setResults={() => setResultsData(null)} />
      ) : (
        <>
          <Text fontSize="2xl" fontWeight="bold" textAlign="center" color="blue.900">Syllabridge</Text>
          <Text fontSize="lg" textAlign="center" color="gray.600">Upload your syllabus and get personalized learning resources</Text>
          <Box w="full">
            <Text fontWeight="bold" mb={2}>Enter your institution:</Text>
            <Input placeholder="e.g., Carnegie Mellon University" value={institution} onChange={e => setInstitution(e.target.value)} />
          </Box>
          <Box w="full">
            <Text fontWeight="bold" mb={2}>Choose a major: <Text as="span" color="red.500">*</Text></Text>
            <Select placeholder="Select a major..." value={major} onChange={e => setMajor(e.target.value)}>
              <option value="cs">Computer Science</option>
              <option value="ee">Electrical Engineering</option>
              <option value="me">Mechanical Engineering</option>
              <option value="math">Mathematics</option>
              <option value="physics">Physics</option>
            </Select>
          </Box>
          <Box w="full">
            <Text fontWeight="bold" mb={2}>Course Information: <Text as="span" color="red.500">*</Text></Text>
            <Grid templateColumns="repeat(2, 1fr)" gap={4}>
              <Input placeholder="e.g., 15112, CS50" value={courseNumber} onChange={e => setCourseNumber(e.target.value)} />
              <Input placeholder="Course Name" value={courseName} onChange={e => setCourseName(e.target.value)} />
            </Grid>
          </Box>
          <Box w="full">
            <Text fontWeight="bold" mb={2}>What is your career goal?</Text>
            <Select placeholder="Select your career goal..." value={futureCareer} onChange={e => setFutureCareer(e.target.value)}>
              <option value="software">Software Engineer</option>
              <option value="research">Research Scientist</option>
              <option value="data">Data Analyst</option>
              <option value="consulting">Consulting</option>
            </Select>
          </Box>
          <Flex w="full" justify="space-between" gap={4}>
            <Box flex={1} p={4} borderWidth={2} borderRadius="lg" borderStyle="dashed" textAlign="center" bg="gray.100">
              <Text fontWeight="bold" color="blue.600">Upload Syllabus File</Text>
              <Input type="file" accept=".pdf,.doc,.docx" onChange={e => setSyllabusFile(e.target.files[0])} mt={2} />
              <Text fontSize="xs" color="gray.500">Supported formats: PDF, DOC, DOCX</Text>
            </Box>
            <Box flex={1} p={4} borderWidth={2} borderRadius="lg" borderStyle="dashed" textAlign="center" bg="gray.100">
              <Text fontWeight="bold" color="blue.600">Or Enter URL</Text>
              <Input placeholder="https://..." value={syllabusUrl} onChange={e => setSyllabusUrl(e.target.value)} mt={2} />
            </Box>
          </Flex>
          <ChakraButton w="full" colorScheme="blue" size="lg" onClick={handleSubmit}>Analyze Syllabus</ChakraButton>
        </>
      )}
    </VStack>
  );
}
