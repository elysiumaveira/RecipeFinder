export interface Difficulty{
    _id: string;
    title: string;
}

export interface Cuisine{
    _id: string;
    title: string;
}

export interface Recipe {
    _id: string;
    title: string;
    ingredients: string[];
    preparation: string;
    cooking_time: number;
    difficulty: Difficulty;
    cuisine: Cuisine;
}