import pandas as pd 
import nepali_datetime 
import re
import datetime 


class url_generator():
  def __init__(self):
    data_path = '/home/ravi/fastapi/fastapi/app/web/blog/article_recommendation/train.csv'
    # self.time_cipher = time_cipher
    # self.url_cipher = url_cipher

    main_df = pd.read_csv(data_path,index_col=False)
    self.url_date_df = main_df[['url','date']] 
    self.url_date_df.date =  self.url_date_df.date.apply(self.to_nepali_date)

    self.most_recent_date = self.url_date_df['date'].max()   
    

  def to_nepali_date(self,date):
    nepali_date = nepali_datetime.datetime.strptime(date.split()[0], '%Y-%m-%d')
    return nepali_date

  

  def filer_by_name(self, url, to_be_filter_url):
    thahakhabar_regex = re.compile('(http[s]?.://.*?thahakhabar.com/)(.*)')
    ratopati_regex = re.compile('(http[s]?://.*?ratopati.com/)(.*)')
    lokaantar_regex = re.compile('(http[s]?://.*?lokaantar.com/)(.*)')
    if to_be_filter_url == 'ratopati':
      # print(url)
      if ratopati_regex.match(url):
        # print(ratopati_regex.match(url).group())
        # return ratopati_regex.match(url).group()
        return True
      else:
        return False
    elif to_be_filter_url == 'thahakhabar':
      if thahakhabar_regex.match(url):
        # print(thahakhabar_regex.match(url).group())
        # return thahakhabar_regex.match(url).group()
        return True
      else:
        return False
    elif to_be_filter_url == 'lokaantar':
      if lokaantar_regex.match(url):
        # print(lokaantar_regex.match(url).group())
        # return lokaantar_regex.match(url).group()
        return True
      else:
        return False

  def filter_by_date(self,df, start_date, end_date):
    mask = (df['date'] > start_date) & (df['date'] <= end_date)
    df = df.loc[mask].reset_index(drop = True)
    return df
      
  def get_df_by_site(self, url_code):
    # print(self.url_cipher[url_code])
    result_df = self.url_date_df[self.url_date_df.apply(lambda x: self.filer_by_name(x['url'], url_code), axis=1)].dropna(axis=0).reset_index(drop = True)
    return result_df

  # def get_df_by_time(self, ):
  #   self.url_date_df.date =  self.url_date_df.date.apply(to_nepali_date)
  #   result_df = self.url_date_df[self.url_date_df.apply(lambda x: self.filer_by_name(x['url'], self.url_filter), axis=1)].dropna(axis=0).reset_index(drop = True)
  #   return result_df

  def get_url_by_time(self, df, time_index):
    end_year = self.most_recent_date.year
    end_month = self.most_recent_date.month
    end_day = self.most_recent_date.day

    end_date = nepali_datetime.datetime(end_year, end_month, end_day, 5, 5, 5, 108108)
    m = re.compile('([\w]+)_([\w]+)').search(time_index)
    start_number = int(m.group(1))
    start_str = m.group(2)

    if start_str == 'days':
      start_date = end_date - datetime.timedelta(days=start_number)
    elif start_str == 'weeks':
      start_date = end_date - datetime.timedelta(weeks=start_number)
    elif start_str == 'months':
      start_date = end_date- datetime.timedelta(days=start_number*30)
      # start_date = end_date - (relativedelta(months=start_number) + timedelta(days=-start_number))
    # elif start_str == 'year':
    #   start_date = end_date - datetime.timedelta(year=start_number)
      # if start_number <  end_month:
      #   start_date = nepali_datetime.datetime(end_year, end_month - start_number, end_day, 5, 5, 5, 108108)
      # else:
      #   start_date = nepali_datetime.datetime(end_year - ((12+start_number)//12), 12 - (start_number - end_month), end_day , 5, 5, 5, 108108)
    else:
      start_date = end_date- datetime.timedelta(days=start_number)
      
    # return (start_date,end_date)
    return self.filter_by_date(df,start_date, end_date)

  def get_url_by_time_only(self,time_index):
    return self.get_url_by_time(self.url_date_df,time_index)
  
  def get_url_by_time_and_site(self, url_code, time_index):
    df = self.get_df_by_site(url_code)
    return self.get_url_by_time(df,time_index)