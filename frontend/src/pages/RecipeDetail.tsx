import { useEffect, useState } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { 
    Typography, 
    Card, 
    Button, 
    Spin, 
    Alert, 
    Tag, 
    List  } from 'antd';
import type { Recipe } from '../types/recipe';
import API from '../config/api';
import getAccesToken from '../utils/getAccessToken';

const { Title, Paragraph } = Typography;

export default function RecipeDetail() {
    const navigate = useNavigate();

    const { id } = useParams<{ id: string }>();
    const [recipe, setRecipe] = useState<Recipe | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!id) return;

        const fetchRecipe = async () => {
            try {
                const response = await API.get(`/recipe-detail/${id}`);
                setRecipe(response.data);
            } catch (error: any) {
                setError('Рецепт не найден!');
            } finally {
                setLoading(false);
            }
        };

        fetchRecipe();
    }, [id]);

    const handleDelete = async () => {
        try {
            await API.delete(`/recipe-delete/${recipe?._id}`, {withCredentials: true});
            navigate('/');
        } catch (error) {
            console.log(error)
        }
    }

    if (loading) {
        return (
            <div style={{ textAlign: 'center', marginTop: 50 }}>
                <Spin size='large' />
                <p>Загрузка</p>
            </div>
        )
    }

    if (error || !recipe) {
        return (
            <Alert
                message='Ошибка'
                description={error}
                type='error'
                showIcon
                style={{ marginBottom: 20 }}
            />
        );
    }

    return (
        <div>
            <Link to="/">
                <Button type="link" color='primary' variant='solid' style={{ margin: 8}}>
                    Назад к списку
                </Button>
            </Link>
            <Link to={`/edit-recipe/${recipe?._id}`}>
                <Button color='orange' variant='solid' style={{ margin: 8 }}>
                    Изменить
                </Button>
            </Link>
            <Button color='red' variant='solid' style={{ margin: 8 }} onClick={handleDelete}>
                Удалить
            </Button>

            <Card
                title={<Title level={2}>{recipe.title}</Title>}
                style={{ marginBottom: 20 }}
            >
                <Paragraph>
                    <strong>Кухня:</strong>{' '}
                    <Tag color="geekblue">{recipe.cuisine.title}</Tag>
                </Paragraph>

                <Paragraph>
                    <strong>Сложность:</strong>{' '}
                    <Tag 
                        color={
                            recipe.difficulty.title === 'Легко' ? 'success' : 
                            recipe.difficulty.title === 'Средняя' ? 'warning' : 'error'
                        }>
                            {recipe.difficulty.title}
                    </Tag>
                </Paragraph>

                <Paragraph>
                    <strong>Время приготовления:</strong> {recipe.cooking_time} мин
                </Paragraph>

                <Paragraph>
                    <strong>Ингредиенты:</strong>
                    <List
                        size="small"
                        dataSource={recipe.ingredients}
                        renderItem={(item) => <List.Item>{item}</List.Item>}
                        style={{ marginTop: 10 }}
                    />
                </Paragraph>

                <Paragraph>
                    <strong>Приготовление:</strong>
                    <div style={{ 
                        padding: '10px', 
                        backgroundColor: '#f9f9f9', 
                        borderRadius: 4, 
                        marginTop: 8 
                    }}>
                        {recipe.preparation}
                    </div>
                </Paragraph>
            </Card>
        </div>
    );
}