import { Box, List, ListItem, Link, Text, Button, Grid, Tag, Image } from '@chakra-ui/react';

export default function Results({ data = [], setResults }) {
  if (!Array.isArray(data)) {
    return (
      <Box bg="white" p={6} borderRadius="lg" boxShadow="lg" mt={6}>
        <Text fontWeight="bold" color="red.500">Invalid data format received.</Text>
        <Button mt={4} colorScheme="red" onClick={() => setResults(null)}>Close</Button>
      </Box>
    );
  }

  return (
    <Grid templateColumns="repeat(2, 1fr)" gap={6} bg="white" p={6} borderRadius="lg" boxShadow="lg" mt={6}>
      <Box>
        <Text fontWeight="bold" fontSize="lg" mb={4}>Learning Resources</Text>
        {data.length > 0 ? (
          data.map((topicData, index) => (
            <Box key={index} mb={6}>
              <Text fontWeight="bold" fontSize="md" color="blue.600">{topicData.topic}</Text>
              <List spacing={3}>
                {topicData.links?.map((link, idx) => (
                  <ListItem key={idx}>
                    <Link href={link} color="blue.500" isExternal>{link}</Link>
                  </ListItem>
                ))}
              </List>
              <Text fontWeight="bold" mt={4}>Video Lectures</Text>
              <List spacing={3}>
                {topicData.video_links?.map((video, idx) => (
                  <ListItem key={idx} display="flex" alignItems="center">
                    <Image src={video.thumbnail} alt={video.title} boxSize="100px" mr={4} />
                    <Box>
                      <Link href={video.url} color="blue.500" isExternal fontWeight="bold">{video.title}</Link>
                      <Text fontSize="sm" color="gray.600">{video.description}</Text>
                      <Text fontSize="xs" color="gray.500">{video.views} views</Text>
                    </Box>
                  </ListItem>
                ))}
              </List>
            </Box>
          ))
        ) : (
          <Text>No results found.</Text>
        )}
      </Box>
      <Button mt={4} colorScheme="red" onClick={() => setResults(null)}>Close</Button>
    </Grid>
  );
}
