import defaultQuestions from './questions/questions.json';
import questions1 from './questions/questions1.json';
import questions2 from './questions/questions2.json';
import questions3 from './questions/questions3.json';

// Map of exam types to question data
export const examData = {
  default: {
    title: "MongoDB Exam 1",
    questions: defaultQuestions
  },
  1: {
    title: "MongoDB Exam 2",
    questions: questions1
  },
  2: {
    title: "MongoDB Querying Exam", 
    questions: questions2
  },
  3: {
    title: "MongoDB Aggregation Exam",
    questions: questions3
  }
};

// Get available exam types
export const getExamTypes = () => {
  return Object.keys(examData).map(key => ({
    value: key === 'default' ? 'default' : key,
    label: examData[key].title
  }));
};

// Get questions by exam type
export const getQuestions = (examType = 'default') => {
  return examData[examType]?.questions || defaultQuestions;
};
