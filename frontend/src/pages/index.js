// pages/index.js
import { ChakraProvider, Container, Flex, Box, Button, Text } from '@chakra-ui/react';
import Header from '../components/Header';
import Form from '../components/Form';
import Results from '../components/Results';
import History from '../components/History';
import { useState } from 'react';

export default function Home() {
  const [results, setResults] = useState(null);
  const [history, setHistory] = useState([]);
  const [showForm, setShowForm] = useState(true);
  const [formCompleted, setFormCompleted] = useState(false);

  const handleSetResults = (newResults) => {
    if (newResults && newResults.courseName && newResults.courseNumber) {
      setResults(newResults);
      setShowForm(false);
      setFormCompleted(true);
      setHistory(prevHistory => [
        { ...newResults, courseName: newResults.courseName, courseNumber: newResults.courseNumber },
        ...prevHistory
      ]);
    }
  };

  return (
    <ChakraProvider>
      <Flex>
        <Box w="25%" p={5} bg="gray.100" minH="100vh" borderRight="1px solid gray.200">
          <Text fontSize="lg" fontWeight="bold" mb={4}>Search History</Text>
          <History history={history} setResults={(selectedResult) => {
            setResults(selectedResult);
            setShowForm(false);
          }} />
        </Box>
        <Container maxW="container.lg" p={10} bg="gray.50" borderRadius="lg" boxShadow="xl" position="relative">
          {showForm ? (
            <>
              <Header />
              <Form setResults={handleSetResults} />
            </>
          ) : (
            <Results data={results} setResults={() => { setResults(null); setShowForm(true); }} />
          )}
          {formCompleted && !showForm && (
            <Button 
              position="absolute" 
              bottom={4} 
              left={4} 
              colorScheme="blue" 
              onClick={() => setShowForm(true)}
            >
              Open Form
            </Button>
          )}
        </Container>
      </Flex>
    </ChakraProvider>
  );
}