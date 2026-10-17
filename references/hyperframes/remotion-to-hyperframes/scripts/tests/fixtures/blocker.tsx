import {useState, useReducer, useEffect} from 'react';
export const Blocker = () => {
  const [value] = useState(0);
  useReducer((state: number) => state + 1, 0);
  useEffect(() => console.log(value), [value]);
  return <div>{value}</div>;
};