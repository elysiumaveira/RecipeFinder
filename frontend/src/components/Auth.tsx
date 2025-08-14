import { useKeycloak } from '@react-keycloak/web';
import { Button } from 'antd';


export default function AuthComponent() {
    const { keycloak, initialized } = useKeycloak();
    
    // Подробная диагностика
    console.log('=== KEYCLOAK STATE ===');
    console.log('initialized:', initialized);
    console.log('authenticated:', keycloak?.authenticated);
    console.log('token exists:', !!keycloak?.token);
    console.log('token parsed:', keycloak?.tokenParsed);
    console.log('refresh token exists:', !!keycloak?.refreshToken);
    console.log('=====================');
    
    // if (!initialized) {
    //     return <div>Загрузка аутентификации...</div>;
    // }
    
    return (
        <div>
            {keycloak?.authenticated ? (
                <Button onClick={() => keycloak.logout()}>
                    Выйти ({keycloak.tokenParsed?.preferred_username || 'Пользователь'})
                </Button>
            ) : (
                <Button onClick={() => keycloak.login()}>
                    Войти через Keycloak
                </Button>
            )}
        </div>
    );
}