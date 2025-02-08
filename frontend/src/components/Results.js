import { Box, List, ListItem, Link, Text, Button, Grid, Tag } from '@chakra-ui/react';

export default function Results({ data = {}, setResults }) {
  return (
    <Grid templateColumns="repeat(2, 1fr)" gap={6} bg="white" p={6} borderRadius="lg" boxShadow="lg" mt={6}>
      <Box>
        <Text fontWeight="bold" fontSize="lg" mb={4}>Learning Resources</Text>
        <Text fontWeight="bold">Similar Courses</Text>
        <List spacing={3}>
          {data.similarCourses?.map((course, index) => (
            <ListItem key={index}>
              <Link href={course.url} color="blue.500" isExternal>{course.title}</Link>
              <Text fontSize="sm" color="gray.600">{course.description}</Text>
            </ListItem>
          ))}
        </List>
        <Text fontWeight="bold" mt={4}>Video Lectures</Text>
        <List spacing={3}>
          {data.videoLectures?.map((lecture, index) => (
            <ListItem key={index}>{lecture}</ListItem>
          ))}
        </List>
        <Text fontWeight="bold" mt={4}>Online Courses</Text>
        <List spacing={3}>
          {data.onlineCourses?.map((course, index) => (
            <ListItem key={index}>{course}</ListItem>
          ))}
        </List>
        <Text fontWeight="bold" mt={4}>Additional Reading</Text>
        <List spacing={3}>
          {data.additionalReading?.map((reading, index) => (
            <ListItem key={index}>{reading}</ListItem>
          ))}
        </List>
      </Box>
      <Box>
        <Text fontWeight="bold" fontSize="lg" mb={4}>Syllabus Analysis</Text>
        <Text fontWeight="bold">Extracting course contents...</Text>
        <Text>Main topics identified:</Text>
        <List spacing={2}>
          {data.topics?.map((topic, index) => (
            <Tag key={index} colorScheme="blue" m={1}>{topic}</Tag>
          ))}
        </List>
        <Text fontWeight="bold" mt={4}>Areas for improvement:</Text>
        <List spacing={2}>
          {data.improvementAreas?.map((area, index) => (
            <ListItem key={index}>• {area}</ListItem>
          ))}
        </List>
        <Text fontWeight="bold" mt={4}>Career-relevant skills ({data.careerPath || 'N/A'}):</Text>
        <Text>Technical skills needed:</Text>
        <List spacing={2}>
          {data.technicalSkills?.map((skill, index) => (
            <Tag key={index} colorScheme="blue" m={1}>{skill}</Tag>
          ))}
        </List>
        <Text fontStyle="italic" mt={4}>Analyzing more details...</Text>
      </Box>
      <Button mt={4} colorScheme="red" onClick={() => setResults(null)}>Close</Button>
    </Grid>
  );
}