const tokenNode = document.getElementById('token');
const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);

function MyApp() {
    const [newToken, setNewToken] = React.useState(null);

    React.useEffect(() => {
        if (!newToken || !tokenNode) {
            return;
        }

        tokenNode.innerHTML = newToken;
    }, [newToken]);

    const requestNewToken = () => {
        $.post(
            '/accounts/update-token-ajax/',
            {csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()}
        ).done(({key}) => {
            setNewToken(key);
        })
    }

    return <button type="button" onClick={requestNewToken}>Сгенерировать новый токен</button>;
}

root.render(<MyApp/>);