import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Typography } from 'antd';
import Home from './pages/Home';
import RecipeDetail from './pages/RecipeDetail';
import AddRecipe from './pages/AddRecipe';
import EditRecipe from './pages/EditRecipe';

const { Header, Content } = Layout;
const { Title } = Typography;

function App() {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ textAlign: 'center' }}>
          <Title level={3} style={{ margin: 14 }} >
            <Link to='/' style={{ color: 'white' }}> 
              Книга рецептов
            </Link>
          </Title>
        </Header>
        <Content style={{ width: '100%' }}>
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/recipe/:id' element={<RecipeDetail />} />
            <Route path='/add-recipe' element={<AddRecipe />} />
            <Route path='/edit-recipe/:id' element={<EditRecipe />} />
          </Routes>
        </Content>
      </Layout>
    </Router>
  )
}

export default App;