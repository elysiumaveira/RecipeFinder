import { useEffect, useState, } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Button, message, Alert, Spin } from 'antd';
import API from '../config/api';
import type { Difficulty, Cuisine } from '../types/recipe';

import CustomInput from '../components/CustomInput/CustomInput';
import CustomSelect from '../components/CustomSelect/CustomSelect';

export default function EditRecipe() {
    const { id } = useParams<{ id: string }>();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null)

    const [title, setTitle] = useState('');
    const [ingredients, setIngredients] = useState<string[]>([]);
    const [preparation, setPreparation] = useState('');
    const [cookingTime, setCookingTime] = useState<string | null>(null);
    const [difficulty, setDifficulty] = useState<Difficulty[]>([]);
    const [difficultyID, setDifficultyID] = useState<string | null>(null)
    const [cuisine, setCuisine] = useState<Cuisine[]>([]);
    const [cuisineID, setCuisineID] = useState<string | null>(null)

    useEffect(() => {
        if (!id) return;

        const fetchAllData = async () => {
            try {
                await Promise.all([
                    fetchRecipe(),
                    fetchDifficulty(),
                    fetchCuisines(),
                ]);
            } catch (error) {
                setError('Произошла ошибка при загрузке данных');
                console.error('Ошибка:', error);
            } finally {
                setLoading(false);
            }
        };

        const fetchRecipe = async () => {
            try {
                const response = await API.get(`/recipe-detail/${id}`);

                setTitle(response.data.title)
                setIngredients(response.data.ingredients)
                setPreparation(response.data.preparation)
                setCookingTime(response.data.cooking_time)
                setDifficultyID(response.data.difficulty._id)
                setCuisineID(response.data.cuisine._id)

                console.log(response.data.difficulty)
            } catch (error) {
                setError('Рецепт не найден!');
                throw error;
            }
        };

        const fetchDifficulty = async () => {
            try {
                const response = await API.get('/difficulties-list');
                if (!response.data) {
                    throw new Error('Нет данных в ответе!');
                }

                const formattedData = Array.isArray(response.data)
                    ? response.data
                    : [response.data];
                
                setDifficulty(formattedData);
            } catch (error) {
                setError('Не удалось загрузить уровни сложности');
                console.log(`Ошибка с загрузкой уровней сложности: ${error}`);
                throw error;
            }
        };

        const fetchCuisines = async () => {
            try {
                const response = await API.get('/cuisines-list');
                if (!response.data) {
                    throw new Error('Нет данных в ответе!');
                }

                const formattedData = Array.isArray(response.data)
                    ? response.data
                    : [response.data];

                setCuisine(formattedData);
            } catch (error) {
                setError('Не удалось загрузить виды кухонь');
                console.log(`Ошибка с загрузкой видов кухонь: ${error}`);
                throw error;
            }
        };

        fetchAllData();
}, [id]);

    const navigate = useNavigate()

    const handleChangeDifficulty = (value: string) => {
        setDifficultyID(value);
    }

    const handleChangeCuisine = (value: string) => {
        setCuisineID(value);
    }

    const handleSubmit = async () => {
        if (!title.trim()) {
            message.error('Введите название');
            return;
        }
        if (ingredients.length === 0) {
            message.error('Добавьте хотя бы один ингредиент');
            return;
        }
        if (!preparation.trim()) {
            message.error('Введите способ приготовления');
            return;
        }
        if (cookingTime === null || Number(cookingTime) <= 0) {
            message.error('Введите корректное время приготовления');
            return;
        }

        const newRecipe = {
            title: title,
            ingredients:ingredients,
            preparation: preparation,
            cooking_time: Number(cookingTime),
            difficulty: difficultyID,
            cuisine: cuisineID,
        };

        try {
            const response = await API.patch(`/recipe-update/${id}`, newRecipe);
            message.success('Рецепт успешно добавлен!');
            navigate(`/recipe/${response.data._id}`);
        } catch (error: any) {
            console.error('Ошибка при создании рецепта:', error);
            message.error('Не удалось добавить рецепт. Проверьте сервер.');
        }
    };

    if (loading) {
        return (
            <div style={{ textAlign: 'center', marginTop: 50 }}>
                <Spin size='large' />
                <p>Загрузка</p>
            </div>
        )
    }

    if (error) {
        return (
            <Alert
                message='Ошибка'
                description={error}
                type='error'
                showIcon
                style={{ marginBottom: 20 }}
            />
        )
    }

    return(
        <div>
            <CustomInput
                placeholder='Название'
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
            />
            <CustomInput
                placeholder='Ингредиенты'
                value={ingredients}
                onChange={(e) => setIngredients(e.target.value.split(','))}
                required
            />
            <CustomInput
                placeholder='Процесс приготовления'
                value={preparation}
                onChange={(e) => setPreparation(e.target.value)}
                required
            />
            <CustomInput
                placeholder='Количество минут'
                value={Number(cookingTime)}
                type='number'
                onChange={(e) => setCookingTime(e.target.value)}
                required
            />
            <CustomSelect
                placeholder='Выберите уровень сложности'
                value={difficultyID}
                onChange={handleChangeDifficulty}
                options={
                    difficulty.map(d => ({
                        value: d._id,
                        label: d.title
                    }))
                }
            />
            <CustomSelect
                placeholder='Выберите вид кухни'
                value={cuisineID}
                onChange={handleChangeCuisine}
                options={
                    cuisine.map((c) => ({
                        value: c._id,
                        label: c.title
                    }))
                }
            />
            <div style={{ 
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                margin: '20px 0'
            }}>
                <Link to='#'>
                    <Button variant='solid' color='red' style={{ width:100, height:45, margin: 5 }} onClick={() => navigate(-1)}>
                        Отмена
                    </Button>
                </Link>
                <Button onClick={handleSubmit} variant='solid' color='green' style={{ width: 100, height:45, margin: 5 }}>
                    Обновить
                </Button>
            </div>
        </div>
    )
}