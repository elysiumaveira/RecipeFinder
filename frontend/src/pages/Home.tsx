import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import type { Difficulty, Cuisine, Recipe } from '../types/recipe';
import API from '../config/api';
import { List, Typography, Spin, Alert, Button, Select, Input } from 'antd';
import RecipeCard from '../components/RecipeCard';
import { useKeycloak } from '@react-keycloak/web';
import AuthComponent from '../components/Auth';

const { Title } = Typography;

export default function Home() {
    const { keycloak, initialized } = useKeycloak();
    const [recipes, setRecipes] = useState<Recipe[]>([]);
    const [difficulties, setDifficulties] = useState<Difficulty[]>([])
    const [difficulty, setDifficulty] = useState<string | null>(null)
    const [cuisines, setCuisines] = useState<Cuisine[]>([])
    const [cuisine, setCuisine] = useState<string | null>(null)
    const [minTime, setMinTime] = useState<Number | null>(null)
    const [maxTime, setMaxTime] = useState<Number | null>(null)
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null)
    const [includeIngredients, setIncludeIngredients] = useState<string[] | null>([])
    const [excludeIngredients, setExcludeIngredients] = useState<string[] | null>([])

    const navigate = useNavigate()

    useEffect(() => {
        const fetchAllData = async () => {
            try {
                await Promise.all([
                    fetchRecipes(),
                    fetchDifficulty(),
                    fetchCuisines(),
                ])
            } catch (error) {
                setError('Произошла ошибка при загрузке данных');
                console.error('Ошибка:', error);
            } finally {
                setLoading(false);
            }
        }
        const fetchRecipes = async () => {
            try {
                const response = await API.get('/recipes-list');
                setRecipes(response.data);
            } catch (error: any) {
                setError('Не удалось загрузить рецепты!');
                console.log(error)
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
                
                setDifficulties(formattedData);
            } catch (error) {
                setError('Не удалось загрузить уровни сложности');
                console.log(`Ошибка с загрузкой уровней сложности: ${error}`);
                throw error;
            }
        }

        const fetchCuisines = async () => {
            try {
                const response = await API.get('/cuisines-list');
                if (!response.data) {
                    throw new Error('Нет данных в ответе!');
                }

                const formattedData = Array.isArray(response.data)
                    ? response.data
                    : [response.data];

                setCuisines(formattedData);
            } catch (error) {
                setError('Не удалось загрузить виды кухонь');
                console.log(`Ошибка с загрузкой видов кухонь: ${error}`);
                throw error;
            }
        };

        fetchAllData();
    }, []);

    const handleChangeCuisine = (value: string | null) => {
        setCuisine(value);
    }

    const handleChangeDifficulty = (value: string | null) => {
        setDifficulty(value);
    }

    const filter = async () => {
        setLoading(true);
        setError(null);

        try {            
            const params = new URLSearchParams()
            
            if(includeIngredients) {
                for (let ing = 0; ing < includeIngredients.length; ing++  ){
                    params.append('include_ingredients', includeIngredients[ing])
                }
            }

            if(excludeIngredients) {
                for (let ing = 0; ing < excludeIngredients.length; ing++  ){
                    params.append('exclude_ingredients', excludeIngredients[ing])
                }
            }

            if(difficulty) params.append('difficulty', difficulty)
            if(cuisine) params.append('cuisine', cuisine)
            if(minTime) params.append('min_cooking_time', String(minTime))
            if(maxTime) params.append('max_cooking_time', String(maxTime))

            const response = await API.get(`/recipes/filter`, { params });
            setRecipes(response.data)
        } catch (error) {
            setRecipes([])
        } finally {
            setLoading(false);
        }
    }

    const resetFilter = async () => {
        setDifficulty(null);
        setCuisine(null);
        setMinTime(null);
        setMaxTime(null);
        setIncludeIngredients([]);
        setExcludeIngredients([]);

        try {
            const response = await API.get('/recipes-list');
            setRecipes(response.data);
        } catch (error) {
            setError('Не удалось загрузить рецепты!');
            console.log(error)
        } finally {
            setLoading(false);
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

    const handleLogin = async () => {
        try {
            // keycloak.login({
            //     redirectUri: window.location.origin
            // })
            window.location.href = 'http://localhost:8000/auth/login'
        } catch (error) {
            setError('Ошибка')
            console.log(error)
        }
        // window.location.href = 'http://localhost:8000/auth/login'
        // window.location.href = `${API.get('/auth/login')}`
    }

    const hanldeLogout = async () => {
        try {
            keycloak.logout({
                redirectUri: window.location.origin
            })
        } catch (error) {
            setError('Ошибка')
            console.log(error)
        }
    }

    // const isAuthenticated = keycloak?.authenticated;
    console.log('Keycloak initialized:', initialized);
    console.log('Keycloak authenticated:', keycloak?.authenticated);
    console.log('Keycloak token:', keycloak?.token ? 'Present' : 'Missing');

    return (
        <>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Title level={2}>Все рецепты</Title>
                <div>
                    {/* {keycloak?.authenticated ? (
                        <Button onClick={hanldeLogout}>
                            Выйти
                        </Button>
                    ) : (
                        <Button onClick={handleLogin}>
                            Войти
                        </Button>
                    )} */}

                    <AuthComponent />

                    <Select
                        placeholder='Фильтр по кухне'
                        onChange={handleChangeCuisine}
                        options={
                            cuisines.map((c) => ({
                                value: c._id,
                                label: c.title
                            }))
                        }
                        value={cuisine}
                        style={{ width: 200 }}
                    />
                    <Select
                        placeholder='Фильтр по сложности'
                        onChange={handleChangeDifficulty}
                        options={
                            difficulties.map((d) => ({
                                value: d._id,
                                label: d.title
                            }))
                        }
                        value={difficulty}
                        style={{ width: 200 }}
                    />
                    <Input
                        placeholder='От (мин)'
                        type='number'
                        onChange={(e) => setMinTime(Number(e.target.value))}
                        style={{ width: 100 }}
                    />
                    <Input 
                        placeholder='До (мин)'
                        type='number'
                        onChange={(e) => setMaxTime(Number(e.target.value))}
                        style={{ width: 100 }}
                    />
                    <Input
                        placeholder='Включить ингредиенты'
                        style={{ width: 200 }}
                        onChange={(e) => setIncludeIngredients(e.target.value.split(', '))}
                    />
                    <Input 
                        placeholder='Исключить ингредиенты'
                        style={{ width: 200 }}
                        onChange={(e) => setExcludeIngredients(e.target.value.split(', '))}
                    />

                    <Button onClick={resetFilter}>
                        Сбросить фильтр
                    </Button>
                    <Button onClick={filter}>
                        Фильтровать
                    </Button>
                </div>
                <Link to={'/add-recipe'} >
                    <Button variant='solid' color='green'>
                        Создать рецепт
                    </Button>
                </Link>
            </div>
            <List
                grid={{ gutter: 16 }}
                dataSource={recipes}
                renderItem={(recipe) => (
                    <List.Item>
                        <RecipeCard recipe={recipe} />
                    </List.Item>
                )}
                locale={{ emptyText:'Рецептов пока нет' }}
            />
        </>
    )
}
