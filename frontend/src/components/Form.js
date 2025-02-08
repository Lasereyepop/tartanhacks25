import { useState } from 'react';
import { Box, Input, Select, VStack, Grid, Text, Flex } from '@chakra-ui/react';
import Button from './Button';

export default function Form({ setResults }) {
  const [institution, setInstitution] = useState('');
  const [major, setMajor] = useState('');
  const [courseNumber, setCourseNumber] = useState('');
  const [courseName, setCourseName] = useState('');
  const [futureCareer, setFutureCareer] = useState('');
  const [syllabusFile, setSyllabusFile] = useState(null);
  const [syllabusUrl, setSyllabusUrl] = useState('');

  const handleSubmit = () => {
    const mockResults = {
      courseName,
      courseNumber,
      futureCareer,
      links: [
        { title: "Introduction to AI", url: "https://ai-course.com" },
        { title: "Machine Learning Basics", url: "https://ml-course.com" }
      ],
      text: "This course provides foundational AI concepts, including machine learning and neural networks."
    };
    setResults(mockResults);
  };

  return (
    <VStack spacing={6} bg="white" p={8} borderRadius="lg" boxShadow="lg">
      <Box w="full">
        <Text fontWeight="bold" mb={2}>Enter your institution:</Text>
        <Input placeholder="e.g., Stanford University" value={institution} onChange={e => setInstitution(e.target.value)} />
      </Box>
      <Box w="full">
        <Text fontWeight="bold" mb={2}>Choose a major:</Text>
        <Select placeholder="Select a major..." value={major} onChange={e => setMajor(e.target.value)}>
          <option value="cs">Computer Science</option>
          <option value="ee">Electrical Engineering</option>
          <option value="me">Mechanical Engineering</option>
          <option value="math">Mathematics</option>
          <option value="physics">Physics</option>
        </Select>
      </Box>
      <Box w="full">
        <Text fontWeight="bold" mb={2}>Course Information:</Text>
        <Grid templateColumns="repeat(2, 1fr)" gap={4}>
          <Input placeholder="Course Number (e.g., CS101)" value={courseNumber} onChange={e => setCourseNumber(e.target.value)} />
          <Input placeholder="Course Name" value={courseName} onChange={e => setCourseName(e.target.value)} />
        </Grid>
      </Box>
      <Box w="full">
        <Text fontWeight="bold" mb={2}>Future Career:</Text>
        <Input placeholder="e.g., Software Engineer" value={futureCareer} onChange={e => setFutureCareer(e.target.value)} />
      </Box>
      <Button text="Analyze Syllabus" onClick={handleSubmit} />
    </VStack>
  );
}
