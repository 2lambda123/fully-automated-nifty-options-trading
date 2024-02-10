from datetime import date, timedelta,datetime
import calendar
import numpy as np
import common.message as m
from time import sleep
import re
z=0
driver=0

def send_variables(a,d):
    """Sends two variables to global scope.
    Parameters:
        - a (any): Variable to be sent to global scope.
        - d (any): Variable to be sent to global scope.
    Returns:
        - None: Does not return any value.
    Processing Logic:
        - Assigns value of a to global variable z.
        - Assigns value of d to global variable driver."""
    
    global z
    global driver 
    z=a
    driver=d
def thursday():
    """Function to return a list of Thursdays for the current and next month.
    Parameters:
        - None
    Returns:
        - thismonth (list): List of Thursdays for the current month.
        - nextmonth (list): List of Thursdays for the next month.
    Processing Logic:
        - Get current year using datetime module.
        - Create a TextCalendar object for Thursdays.
        - Loop through current and next month to find all Thursdays.
        - Append Thursdays to respective lists.
        - Remove past Thursdays from current month list.
        - Return both lists of Thursdays."""
    
    now=datetime.datetime.now()
    Year=now.year
    A=calendar.TextCalendar(calendar.THURSDAY)
    thismonth=[]
    nextmonth=[]
    for b in range(now.month,now.month+2):
        thismonth=nextmonth.copy()
        nextmonth=[]
        for k in A.itermonthdays(Year,b):
            if k!=0:
                day=date(Year,b,k)
                if day.weekday()==3:
                    #print("%s,%d-%d-%d" % (calendar.day_name[3] ,k,b,Year))
                    nextmonth.append(k)
    thismonth1=[]
    for i in range(len(thismonth)):
        if thismonth[i]>now.date().day:
            thismonth1.append(thismonth[i])   
    thismonth=thismonth1          
    return thismonth,nextmonth

def option_names(strike_price,ceorpe):
    """Parameters:
        - strike_price (int): The strike price for the option.
        - ceorpe (str): Whether the option is a call or put.
    Returns:
        - list: A list of option names for the current and next month.
    Processing Logic:
        - Generates a list of option names.
        - Uses the current and next month.
        - Includes the strike price and call/put designation.
        - Returns the list of option names."""
    
    thismonth,nextmonth=thursday()
    now=datetime.datetime.now()
    this=now.strftime('%b').upper()
    tt=now+timedelta(30)
    next=tt.strftime('%b').upper()
    this_name=[]
    for i in range(len(thismonth)):
        this_name.append(f'NIFTY {thismonth[i]}th w {this} {strike_price} {ceorpe}')
    this_name.pop()
    this_name.append(f'NIFTY {this} {strike_price} {ceorpe}')    
    next_name=[]
    for i in range(len(nextmonth)):
        next_name.append(f'NIFTY {nextmonth[i]}th w {next} {strike_price} {ceorpe}')
    next_name.pop()
    next_name.append(f'NIFTY {next} {strike_price} {ceorpe}')  
    this_name.extend(next_name)
    return this_name

def select_strike_price(ltp):
    """"Rounds the last traded price to the nearest multiple of 50."
    Parameters:
        - ltp (float): Last traded price of a stock.
    Returns:
        - float: Rounded value of the last traded price.
    Processing Logic:
        - Rounds to the nearest multiple of 50.
        - Uses the round() function.
        - No decimal places in the return value."""
    
    return round(ltp/50)*50

def open_positions():
    """Returns a dictionary of open positions from a trading platform.
    Parameters:
        - z (object): Trading platform object.
    Returns:
        - open_pos (dict): Dictionary of open positions.
    Processing Logic:
        - Get positions from trading platform.
        - Create an empty dictionary.
        - Loop through positions.
        - Check if position is not a cash and has a non-zero quantity.
        - Add position to dictionary.
        - Return dictionary of open positions."""
    
    bb=z.get_position()
    open_pos=dict()
    try:
        for i in bb:
            if i!='totalpandl':
                if bb[i]['product']!='CNC' and int(bb[i]['qty'])!=0:
                    open_pos[i]=bb[i]

                    print(i)
    except:
        pass      
    return open_pos
def is_option_active():
    """"Checks if any open positions for NIFTY are active."
    Parameters:
        - None
    Returns:
        - bool: True if there are active open positions for NIFTY, False otherwise.
    Processing Logic:
        - Checks if there are any open positions for NIFTY.
        - Returns True if there are, False otherwise."""
    
    try:
        global open_positions_list
        #o=open_positions().keys()
        o=open_positions_list.keys()
        for i in o:
            if 'NIFTY' in i:
                return True
    except Exception as error:
        print(error)
        return False            
    return False        

def check_target(target=0.8):
    """Checks if the average price of open positions is below a certain target percentage of the current market price.
    Parameters:
        - target (float): The target percentage of the current market price. Default value is 0.8.
    Returns:
        - bool: True if the average price of open positions is below the target percentage, False otherwise.
    Processing Logic:
        - Checks if the average price of open positions is below the target percentage.
        - Skips 'totalpandl' in the open positions list.
        - Returns True if the condition is met for any open position, False otherwise.
        - Returns False if there are no open positions."""
    
    global open_positions_list
    #open_pos=open_positions()
    open_pos=open_positions()
    for i in open_pos:
        if i=='totalpandl':
            continue
        if float(open_pos[i]['avg'])*(1-target)>float(open_pos[i]['ltp']):
            return True
        else:
            return False
    return False      

def new_positions():
    """This function calculates new positions based on the old trend and current data.
    Parameters:
        - old_trend (string): The previous trend, either 'up' or 'down'.
    Returns:
        - None: This function does not return anything.
    Processing Logic:
        - Calculate the strike price based on the previous closing price.
        - If the current day is Tuesday or Wednesday, select the second option name.
        - Otherwise, select the first option name.
        - Place a buy order for 50 units of the option with the calculated strike price and type 'PE' or 'CE'.
        - Place a sell order for 50 units of the option with the calculated strike price and type 'PE' or 'CE'."""
    
    if (old_trend=='down') :

        if int(now.strftime('%w'))>2 and int(now.strftime('%w'))<4:
            symbol_sell=option_names(strike_price=select_strike_price(data.iloc[-2]['close']),ceorpe='PE')[1]
            symbol_buy=option_names(strike_price=select_strike_price(data.iloc[-2]['close'])-risk,ceorpe='PE')[1]
        else:
            symbol_sell=option_names(strike_price=select_strike_price(data.iloc[-2]['close']),ceorpe='PE')[0]
            symbol_buy=option_names(strike_price=select_strike_price(data.iloc[-2]['close'])-risk,ceorpe='PE')[0]
        z.place_order(symbol=symbol_buy,qtn=50,transaction_type =ZC.TRANSACTION_TYPE_BUY) 
        #sleep(1)
        z.place_order(symbol=symbol_sell,qtn=50,transaction_type =ZC.TRANSACTION_TYPE_SELL)
        #sleep(1)

    if (old_trend=='up' ) :
        if int(now.strftime('%w'))>2 and int(now.strftime('%w'))<4:
            symbol_sell=option_names(strike_price=select_strike_price(data.iloc[-2]['close']),ceorpe='CE')[1]
            symbol_buy=option_names(strike_price=select_strike_price(data.iloc[-2]['close'])+risk,ceorpe='CE')[1]
        else:
            symbol_sell=option_names(strike_price=select_strike_price(data.iloc[-2]['close']),ceorpe='CE')[0]
            symbol_buy=option_names(strike_price=select_strike_price(data.iloc[-2]['close'])+risk,ceorpe='CE')[0]
        z.place_order(symbol=symbol_buy,qtn=50,transaction_type =ZC.TRANSACTION_TYPE_BUY) 
        #sleep(1)
        z.place_order(symbol=symbol_sell,qtn=50,transaction_type =ZC.TRANSACTION_TYPE_SELL)
        #sleep(1)

def less_risk(risk):
    """Calculates the closest value to half of the given risk from a range of numbers.
    Parameters:
        - risk (int or float): The value of risk to be evaluated.
    Returns:
        - closest_value (int or float): The closest value to half of the given risk from the range of numbers.
    Processing Logic:
        - Creates a list of numbers from 50 to 4950 with a step of 50.
        - Calculates the absolute difference between each number and half of the given risk.
        - Finds the index of the minimum absolute difference.
        - Returns the value at that index from the list of numbers.
    Example:
        less_risk(200) # Returns 150"""
    
    u=[]
    for i in range(1,100):
        u.append(50*i)
    u=np.array(u)
    yy=abs(u-(risk/2))
    mini=10000
    ind=0
    return u[np.argmin(yy)]

def get_sleep_time():
    """"Calculates the next scheduled run time based on the current time, rounding to the nearest 5 minutes."
    Parameters:
        - None
    Returns:
        - datetime: The next scheduled run time, rounded to the nearest 5 minutes.
    Processing Logic:
        - Calculates current time.
        - Rounds current time to nearest 5 minutes.
        - Sets next run time to 5 minutes after rounded time.
        - Returns next run time."""
    
    now = datetime.datetime.now()
    next_run = now.replace(minute=int(now.minute / 5) * 5, second=0, microsecond=0) + datetime.timedelta(minutes=5)
    return next_run


overbought_or_oversold='oversold'

def create_basket():
    """Creates a new basket in the Kite platform.
    Parameters:
        - None
    Returns:
        - bool: True if the basket is successfully created, False otherwise.
    Processing Logic:
        - Clicks on the 'Create Basket' button.
        - Enters the name of the new basket.
        - Clicks on the 'Create' button.
        - If an error occurs, tries again to create the basket."""
    
    global new_basket_name
    if driver.current_url!='https://kite.zerodha.com/orders/baskets':
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/div[1]/a[2]/span').click()
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/a[3]/span').click()
    try:
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div/section/div/div/span[1]/button').click()
    except:
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/button').click()
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[2]/div/form/div[1]/input').send_keys(new_basket_name)
    #sleep(2)
    u=False
    while True:
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[2]/div/form/div[2]/button').click()
            u=True
            break
        except Exception as error:
            print('trying agian to crate basket')
            sleep(1)
        if u:
            break    
    return True
def name_to_price(stock_name):
    """"Converts a stock name to its corresponding price.
    Parameters:
        - stock_name (str): The name of the stock to be converted.
    Returns:
        - float: The price of the stock.
    Processing Logic:
        - Extracts the price from the stock name.
        - Removes any spaces from the price.
        - Removes any letters from the price.
        - Returns the price as a float value.""""
    
    return re.sub(' ','',re.sub('[A-Z]','',stock_name[stock_name.find('w')+6:]))
def add_instruments_basket(stock_names,market=True,qty=50,overnight=True,buy_sell=None):
    """Adds a basket of instruments to the trading platform with specified parameters.
    Parameters:
        - stock_names (list): List of stock names to be added to the basket.
        - market (bool): Optional parameter to specify if the instruments should be added at market price. Default is True.
        - qty (int): Optional parameter to specify the quantity of each instrument to be added. Default is 50.
        - overnight (bool): Optional parameter to specify if the instruments should be held overnight. Default is True.
        - buy_sell (list): Optional parameter to specify the buy/sell action for each instrument. Default is None, which will result in alternating buy/sell actions.
    Returns:
        - True (bool): Indicates successful addition of instruments to the basket.
    Processing Logic:
        - Creates a basket on the trading platform.
        - Iterates through the list of stock names and adds each instrument to the basket.
        - Searches for the strike price of each instrument and selects it.
        - If market parameter is True, selects market price option.
        - Clears the quantity input field and enters the specified quantity.
        - If overnight parameter is True, selects overnight option.
        - If buy_sell parameter is specified, alternates between buy and sell actions for each instrument.
        - Clicks the "Add" button to add the instrument to the basket."""
    
    buy_sell = ['buy','sell'] if buy_sell is None else buy_sell
    create_basket()
    co=0
    for stock_name in stock_names:
        strike_price=name_to_price(stock_name)
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/input').send_keys(strike_price)
        sleep(2)
        try:
            for i in range(1,100):
                s=driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[1]/div/ul/div/li[{i}]/span[1]/span').text
                if s==stock_name:
                    driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[1]/div/ul/div/li[{i}]/span[1]/span').click()
                    break
        except Exception as error:
            print(error)
        if market==True:
            driver.find_element_by_xpath('/html/body/div[1]/form/section/div[2]/div[2]/div[2]/div[2]/div/div[1]/label').click()
        for i in range(10):
            driver.find_element_by_xpath('/html/body/div[1]/form/section/div[2]/div[2]/div[1]/div[1]/div/input').send_keys(Keys.BACKSPACE)                
        driver.find_element_by_xpath('/html/body/div[1]/form/section/div[2]/div[2]/div[1]/div[1]/div/input').send_keys(qty)
        if overnight==True:
            driver.find_element_by_xpath('/html/body/div[1]/form/section/div[2]/div[1]/div/div[2]/label').click()
        if buy_sell[co]=='sell':
            driver.find_element_by_xpath('/html/body/div[1]/form/header/div[1]/div[2]/div/div[2]/span/div/label').click()    
        co+=1
        driver.find_element_by_xpath('/html/body/div[1]/form/section/footer/div[2]/button[1]/span').click()
    return True
def check_margin(stock_names,market=True,overnight=True,close=True,buy_sell=None):
    """"""
    
    buy_sell = ['buy','sell'] if buy_sell is None else buy_sell
    global qty
    add_instruments_basket(stock_names,market,qty,overnight,buy_sell)
    sleep(2)
    margin=dict()
    margin['required_margin']=driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[3]/div/div/div[1]/div/div[1]/div/span').text
    margin['final_margin']=driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[3]/div/div/div[1]/div/div[2]/div/span/span').text
    margin['final_margin']=float(re.sub('[,]','',margin['final_margin']))
    margin['required_margin']=float(re.sub('[,]','',margin['required_margin']))
    if close==True:
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[3]/div/div/div[2]/button[2]').click()
    return margin

def check_max_loss(stock_names,market=True,qty=50,overnight=True):
    """"""
    
    try:
        #stock_names=[symbol_buy,symbol_sell]
        margin=check_margin(stock_names,market=True,overnight=True,close=False)
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[1]/div/div[2]/a[1]/span').click()
        sleep(10)
        summary=dict()
        frame=driver.find_element_by_xpath('/html/body/div[1]/div[6]/div/div/div[2]/div/iframe')
        driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[1]/div[6]/div/div/div[2]/div/iframe'))
        t=driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/div[1]/div[3]/div[2]/div/div').text.split('\n')
        summary=dict()
        for i in range(len(t)):
            if i%2==0:
                try:
                    y=t[i+1]
                    y=re.sub(',','',y)
                    y=re.sub('%','',y)
                    if y=='--':
                        y=None
                    summary[t[i]]=float(y)
                except:
                    summary[t[i]]=t[i+1]  
        driver.get('https://kite.zerodha.com/orders/baskets')
        sleep(5)
        return summary,margin
    except Exception as error:
        print(error)
        driver.get('https://kite.zerodha.com/orders/baskets')
        sleep(5)
        try:
            return summary,margin
        except :
            pass
        #driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/div[1]/div[3]/div[2]/div/div/div[1]/div[2]').text
        #driver.find_element_by_xpath('/html/body/div[1]/div[6]/div/div/div[3]/div/button').click()

def basket_order(stock_names):
    """"""
    
    margin=z.get_margins()
    fund= margin['equity']['Available margin']
    money=check_margin(stock_names,close=False)
    if float(money['required_margin'])>fund:
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[3]/div/div/div[2]/button[2]').click()
        global qty
        if qty>50:
            qty=qty-50 
            m.message('Margin is not enough in your account to trade... trying with less quantity...')
            basket_order(stock_names)
        else:
            m.message('Margin is not enough in your account to trade...') 
    else:
            driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[3]/div/div/div[2]/button[1]').click()
            driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[3]/div/button[1]').click()
            sleep(1)
            plac=driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[2]/div/table/tbody/tr[1]/td[8]/span/span').text
            #driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[3]/div/div/div[2]/button[2]').click()
            try:
                driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[3]/div/div/div[2]/button[2]').click()
            except:
                try:
                    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[3]/div/div/div[2]/button[2]').click()
                except:
                    pass   
                pass
            if plac=='FAILED':
                return False
            return True  

def clean_basket(all=False):
    """"""
    
    global new_basket_name
    u=['/html/body/div[1]/div[1]/div/div[2]/div[1]/a[2]/span','/html/body/div[1]/div[2]/div[2]/div[1]/a[3]/span']
    for i in u:
        driver.find_element_by_xpath(i).click()
    try:
        if all==False:                  
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div/section/div/div/span[2]/div/input').send_keys(new_basket_name)
            sleep(0.5)
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div/section/div/div/span[2]/div/input').send_keys(Keys.ENTER)
        for i in range(1,51):
            el=driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div[2]/div[2]/div/section/div/table/tbody/tr[1]/td[1]')
            #el.location_once_scrolled_into_view
            name=el.text
            if name!=False:
                el=driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div[2]/div[2]/div/section/div/table/tbody/tr[1]/td[1]')
                try:
                    hover = ActionChains(driver).move_to_element(el).perform()
                    #hover.perform()
                    sleep(2)
                    driver.find_element_by_class_name('context-menu').click()
                    sleep(1)
                    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div/section/div/table/tbody/tr[1]/td[1]/div/ul/li[2]/a').click()
                    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[3]/div/button[1]/span').click()
                except:
                    pass 
    except:
        pass 
    sleep(1)     
    try:
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div/section/div/div/span[2]/span[2]').click() 
    except:
        pass    
    return True
now=datetime.now()
def get_strike_price(old_trend, new_trend,ce_or_pe,next=False):
    """"""
    
    if old_trend=='down' and new_trend=='up':                        
        if (int(now.strftime('%w'))>2 and int(now.strftime('%w'))<4) or next==True:
            symbol_sell=option_names(strike_price=select_strike_price(data.iloc[-2]['close']),ceorpe=ce_or_pe)[1]
            symbol_buy=option_names(strike_price=select_strike_price(data.iloc[-2]['close'])-risk,ceorpe=ce_or_pe)[1]
        else:
            symbol_sell=option_names(strike_price=select_strike_price(data.iloc[-2]['close']),ceorpe=ce_or_pe)[0]
            symbol_buy=option_names(strike_price=select_strike_price(data.iloc[-2]['close'])-risk,ceorpe=ce_or_pe)[0]
    if (old_trend=='up' and new_trend=='down') :
        if (int(now.strftime('%w'))>2 and int(now.strftime('%w'))<4) or next==True:
            symbol_sell=option_names(strike_price=select_strike_price(data.iloc[-2]['close']),ceorpe=ce_or_pe)[1]
            symbol_buy=option_names(strike_price=select_strike_price(data.iloc[-2]['close'])+risk,ceorpe=ce_or_pe)[1]
        else:
            symbol_sell=option_names(strike_price=select_strike_price(data.iloc[-2]['close']),ceorpe=ce_or_pe)[0]
            symbol_buy=option_names(strike_price=select_strike_price(data.iloc[-2]['close'])+risk,ceorpe=ce_or_pe)[0]
    return [symbol_buy,symbol_sell]   
def get_best_strike_price(old_trend,new_trend):
    """"""
    
    global uptrend_ce_or_pe
    global downtrend_ce_or_pe
    if old_trend=='down' and new_trend=='up':  
        ceorpe=uptrend_ce_or_pe
    if old_trend=='up' and new_trend=='down':
        ceorpe=downtrend_ce_or_pe
    return get_strike_price(old_trend,new_trend,ceorpe)           

def best_option_selection(next=False):
    """"""
    
    global uptrend_ce_or_pe
    global downtrend_ce_or_pe
    up_pe,margin_up_pe=check_max_loss(get_strike_price('down','up','PE',next),market=True,qty=50,overnight=True)
    up_ce,margin_up_ce=check_max_loss(get_strike_price('down','up','CE',next),market=True,qty=50,overnight=True)  
    down_pe,margin_down_pe=check_max_loss(get_strike_price('up','down','PE',next),market=True,qty=50,overnight=True) 
    down_ce,margin_down_ce=check_max_loss(get_strike_price('up','down','CE',next),market=True,qty=50,overnight=True)            
    if abs(up_pe['Max Loss'])>abs(up_ce['Max Loss']):
        uptrend_ce_or_pe='CE'
        qty_check(margin=margin_up_ce['required_margin'])
    if abs(up_pe['Max Loss'])<abs(up_ce['Max Loss']): 
        uptrend_ce_or_pe='PE'
        qty_check(margin=margin_up_pe['required_margin'])
    if abs(down_pe['Max Loss'])>abs(down_ce['Max Loss']):
        downtrend_ce_or_pe='CE'
        qty_check(margin=margin_down_ce['required_margin'])
    if abs(down_pe['Max Loss'])<abs(down_ce['Max Loss']):
        downtrend_ce_or_pe='PE' 
        qty_check(margin=margin_down_pe['required_margin'])
    return uptrend_ce_or_pe,downtrend_ce_or_pe   
def refresh_every(count):
    global how_refresh_every
    if count/how_refresh_every==round(count/how_refresh_every):
        return True
    else:
        return False
def qty_check(old_trend=None,margin=None):
    global qty
    global qty_fixed_or_not
    if margin==None:
        if old_trend=='up' or old_trend==None:
            u=check_margin(get_best_strike_price('up','down'))['required_margin']
            q=u
        sleep(2)
        try:
            if old_trend=='down' or old_trend==None:
                v=check_margin(get_best_strike_price('down','up'))['required_margin']
                q=v
        except:
            sleep(10)
            v=check_margin(get_best_strike_price('down','up'))['required_margin']  
            q=v
    else:
        u=margin
        v=margin          
    if old_trend==None:
        q=max(u,v)
    f=z.get_margins()['equity']['Available margin']
    newqty=floor(f/q)*50
    if qty>newqty:
        qty=newqty
    if not qty_fixed_or_not:
        qty=newqty
    return newqty

def refresh():
    print('Refreshing'.center(50,'-'))
    clean_basket()
    best_option_selection()
    print('UP Trend : ',get_best_strike_price('down','up'))
    print('Down Trend : ',get_best_strike_price('up','down'))
    print("Updated Quantity is :",qty)
def position_trend():
    global open_positions_list
    try:
        strike=[]
        buyorsell=[]
        for i in open_positions_list:
            strike.append(int(name_to_price(i)))
            buyorsell.append(int(open_positions_list[i]['qty']))
        if buyorsell[strike.index(min(strike))]>0 and buyorsell[strike.index(max(strike))]<0:
            return 'up'
        if buyorsell[strike.index(min(strike))]<0 and buyorsell[strike.index(max(strike))]>0:
            return 'down'   
    except :
        return False                 
        
