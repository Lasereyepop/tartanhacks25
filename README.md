## Syllabridge

#### An AI - Powered Web App that helps students extract essential concepts from syllabi and identify appropriate learning materials.

#### How it works 
1. Enter your class information & career goals
2. Upload your syllabus as a pdf or a url
3. Gain insightful information, cross-comparison to similar courses from highly-ranked universities, and gain insight into career development skills & projects to improve
4. Keep track of your search history and gian unique insights that are class & school specific!
5. Find highly-rated educational videos to supplement your class material

#### Challenges we ran into
This was super fun to develop but we used a diverse amount of libraries & frameworks and getting them to work together was difficult. Furthermore, the speed of our API calls was less than ideal at times. That being said, we achieved functionality and we were impressed by the end product we were able to come up with in such a short period of time

#### Next Steps
1. Multi-Disciplinary support -> Currently a STEM/CS focus, expand into other diciplines
2. Curriculim Mapping -> Visual aid supporting insights, connections of topics between classes using a graph-like structure.
3. Curriculim Optimization Tool -> Decide which classes to take based off of your interests, previous coursework, and class material.


To run the backend,
1. create a python venv
2. `pip install -r requirements.txt`
3. run `python -m uvicorn api:app --reload`


To run the frontend,
Then run ```npm install next react react-dom```
Then run ```npm audit fix```
Then run ```npm run build```
Then run ```npm run dev```
