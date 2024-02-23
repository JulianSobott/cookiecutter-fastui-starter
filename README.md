# Cookiecutter FastUI Starter Template

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), this project shows how to use [FastUI](https://github.com/pydantic/FastUI) with a custom component.

## Requirements

- [Python](https://www.python.org/downloads/): `>=3.10` (older versions can work, but are not tested)
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter): `pipx install cookiecutter`
- [Poetry](https://python-poetry.org/): `pipx install poetry`
- [Node.js](https://nodejs.org/en/): `>=v18.16.1`
- [npm](https://www.npmjs.com/): `>=9.5.1`

## Setup

```bash
# Create a new project from the template
cookiecutter gh:JulianSobott/cookiecutter-fastui-starter
# Change into the new directory (adjust the name if you changed it)
cd fastui_starter
# Install python dependencies
poetry install

cd fastui_starter_app
# Install node dependencies
npm install
``` 

## Hot Fix for fastui-bootstrap (temporary fix until the package is updated)

Since something is wrong with the `fastui-bootstrap` package, you need to adjust it manually.\
In `fastui_starter_app/node_modules/@pydantic/fastui-bootstrap.package.json` change the following lines:

```diff
{
  "name": "@pydantic/fastui-bootstrap",
  "version": "0.0.22",
  "description": "Boostrap renderer for FastUI",
- "main": "dist/index.js",
+ "main": "dist/npm-fastui-bootstrap/src/index.js",
- "types": "dist/index.d.ts",
+ "types": "dist/npm-fastui-bootstrap/src/index.d.ts",
```

Final file should start like this:

```json
{
  "name": "@pydantic/fastui-bootstrap",
  "version": "0.0.22",
  "description": "Boostrap renderer for FastUI",
  "main": "dist/npm-fastui-bootstrap/src/index.js",
  "types": "dist/npm-fastui-bootstrap/src/index.d.ts",
  "author": "Samuel Colvin",
}
```

## Usage in Development

Start backend and frontend with hot-reload.

```bash
# start the backend with reload (adjust fastui_starter to your project name)
poetry run uvicorn fastui_starter_app.main:app --reload
cd fastui_starter_app

# run the frontend in development mode
npm run dev
```

## Usage in Production

```bash
# build frontend
cd fastui_starter_app
npm run build
cd ..
# start backend
poetry run uvicorn fastui_starter_app.main:app
```


## Adding a new component

### Frontend

1. Create a new React function component. For example in `src/App.tsx`
```tsx
const MyComponent: FC<{ text: string }> = ({ text }) => {
  return <div>Message from my own component: {text}</div>;
}
```
2. return it in the `customRender` function in `src/App.tsx`
```tsx
const customRender: CustomRender = (props) => {
  const { type } = props
  // You can name your library whatever you want (e.g. yourLib)
  if (type === 'Custom' && props.library === "yourLib") {
    switch (props.subType) {
      // Add your components here
      case 'MyComponent':
        return () => <MyComponent text={props.data as string} />
      default:
        return bootstrap.customRender(props)
    }
  } else {
    return bootstrap.customRender(props)
  }
}
```

### Backend

1. Use it with the `Custom` class:
```python
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Custom(data='This is a custom component', sub_type="myComponent", library="yourLib"),
            ]
        ),
    ]
```
2. Optionally, you can create a function to generate the `Custom` component:
```python
def my_component(text: str) -> c.Custom:
    return c.Custom(data=text, sub_type="myComponent", library="yourLib")
# ...
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                my_component('This is a custom component'),
            ]
        ),
    ]
```
