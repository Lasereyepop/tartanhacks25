import { Box, List, ListItem, Button } from '@chakra-ui/react';

export default function History({ history, setResults }) {
  return (
    <Box>
      <List spacing={3}>
        {history.map((item, index) => (
          <ListItem key={index}>
            <Button variant="link" onClick={() => setResults(item)}>
              {item.courseName && item.courseNumber ? `${item.courseName} (${item.courseNumber})` : "Unknown Course"}
            </Button>
          </ListItem>
        ))}
      </List>
    </Box>
  );
}