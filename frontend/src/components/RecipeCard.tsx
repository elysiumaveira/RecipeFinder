import React from 'react';
import { Link } from 'react-router-dom';
import type { Recipe } from '../types/recipe';
import { Card, Tag } from 'antd';

interface Props {
    recipe: Recipe;
}

const RecipeCard: React.FC<Props> = ({ recipe }) => {
    return (
        <Card title={recipe.title} extra={<Link to={`recipe/${recipe._id}/`}>Подробнее</Link>} style={{ maxWidth: '450px', height: '100%' }} >
            <p><strong>Ингридиенты:</strong></p>
            <div style={{ marginBottom: 10 }}>
                {recipe.ingredients.map((ing, i) => (
                    <Tag key={i} color='blue'>{ing}</Tag>
                ))}
            </div>

            <p><strong>Приготовление:</strong> {recipe.preparation.substring(0, 90)}...</p>

            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 10 }}>
                <Tag color='green'>{recipe.cooking_time} минут</Tag>
                <Tag color={
                    recipe.difficulty.title === 'Легко' ? 'success' : 
                    recipe.difficulty.title === 'Средняя' ? 'warning' :
                    'error'
                }>
                    {recipe.difficulty.title}
                </Tag>
            </div>
        </Card>
    )
}

export default RecipeCard;