from textwrap import dedent

scatter_markdown = dedent('''
    ##### GDP and FIFA rank for different countries for a single year.

    For changing the year you can move the slider

    From this scatter plot it is visible that countries with higher GDPs tend to have better rank (the rank axis is
    inversed).
''')

rank_lineplot_markdown = dedent('''
    ##### FIFA Rank and GDP of countries through years
    
    You can add or remove countries from the list above.
    
    From graphs of different countries we can see that it through years, usually high gdp implies better rank in FIFA
    table.
    
    Although we saw that there is a high correlation with gdp and FIFA ranking, Not all countries's ranking are that
    dependant from gdp
    
''')

gdp_lineplot_markdown = dedent('''
    
    If we choose countries that have very developed football, we can see that the correlation betwen that county's GDP 
    and FIFA ranking is lower. 
    
    In contrast, Rankings of the countries with still developing football are more dependent from GDP changes.
''')