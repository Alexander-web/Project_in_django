from django.conf import settings
from django.db import models
from django.utils import timezone
import socket

class Keys(models.Model):# Параметры для передачи в ВАЦ
    namber_of_points_for_smoothing=models.IntegerField(null=True,blank=True,default=201, verbose_name="Количество точек сглаживания")
    input_power=models.IntegerField(null=True,blank=True,verbose_name="Входная мощность")
    input_power_first=models.IntegerField(null=True,blank=True,verbose_name="Входная мощность начальная")
    input_power_last=models.IntegerField(null=True,blank=True,verbose_name="Входная мощность конечная")
    width_filter=models.IntegerField(null=True,blank=True,verbose_name="Ширина фильтра ПЧ")
    namber_of_points_for_averaging=models.IntegerField(null=True,blank=True,default=201, verbose_name="Количество точек")
    def __str__(self):
        return f'Кол-во точек сгл:{self.namber_of_points_for_smoothing}; Вх_P:{self.input_power}; Вх_Pнач:{self.input_power_first}; Вх_Pкон:{self.input_power_last}; Ширина_ПЧ:{self.width_filter}; Кол-во_точек:{self.namber_of_points_for_averaging}'

class SpaceCraft(models.Model):
    name = models.CharField(("Наименование КА"), max_length=50)
    def __str__(self):
        return self.id.__str__()+'.'+self.name

class PayLoad(models.Model):
    name = models.CharField(("Наименование РТР"), max_length=50)
    spacecraft = models.ForeignKey("SpaceCraft", verbose_name=("КА"), on_delete=models.CASCADE)
    def __str__(self):
        return self.name

#Менеджер моделей, для FreqRange
class FreqRangeManager(models.Manager):
    def get_queryset(self,freq):
        return super(FreqRangeManager, self).get_queryset().filter(name=freq)

class MeasureType(models.Model):                         #Тип измерерия АЧХ, НГВЗ, точка насыщения, АМ-АМ
    name = models.CharField(max_length=50,verbose_name="Тип измерения")
    key=models.ForeignKey("Keys", verbose_name=("Ключи"), on_delete=models.CASCADE, related_name = 'keys')
    def __str__(self):
        return self.name

class SSI(models.Model):                                    #Конфигурации
    name = models.CharField('Имя SSI',max_length=50, unique=True)                  
    input_frequency = models.FloatField('Входная частота')
    output_frequency = models.FloatField('Выходная частота')
    band_frequency = models.FloatField('Полоса частот')
    available_meas= models.ManyToManyField(MeasureType, related_name='ssi',verbose_name="Тип измерения")
    pay_load=models.ForeignKey(PayLoad,  null=True,blank=True, on_delete = models.CASCADE,related_name = 'pay_load_ssi',verbose_name="Полезная нагрузка")
    def __str__(self):
        return self.name

class FreqRange(models.Model):
    input_range = models.CharField(("Входной диапазон"), max_length=50)
    output_range = models.CharField(("Выходной диапазон"), max_length=50)
    ssi_element =  models.ForeignKey(SSI, on_delete = models.CASCADE,related_name = 'freqrange')
    name=models.CharField(("Имя диапазона"), max_length=50)
    objects=models.Manager()
    custom_manager=FreqRangeManager()
    def __str__(self):
        return f'{str(self.input_range)}/{str(self.output_range)}'

class Measure_que(models.Model):                            # Класс очереди
    date_time = models.DateTimeField(auto_now_add = True)
    ssi = models.ForeignKey(SSI, on_delete = models.CASCADE, verbose_name="Имя SSI")
    meastype = models.ForeignKey(MeasureType, on_delete = models.CASCADE,verbose_name="Тип измерения")
    def __str__(self):
        return 'Имя SSI: {}, Тип измерения: {}, Время измерения: {}'.format(self.ssi, self.meastype, self.date_time)

class Measure(models.Model): 
    class Meta:
        permissions = (("make_measures", "проводит измерения"),)                                 #Класс, собирающий информацию о имени SSI и типе измерения в нем для передачи этой информации в AcceptData
    time = models.DateTimeField(auto_now_add = True)
    ssi = models.ForeignKey(SSI, on_delete = models.CASCADE,related_name='meas', verbose_name="Имя SSI")
    mea = models.ForeignKey(MeasureType, on_delete = models.CASCADE,related_name = 'measure_type',verbose_name="Тип измерения")
    def __str__(self):
        return 'Имя SSI: {}, Тип измерения: {}'.format(self.ssi, self.mea)

class AcceptData(models.Model):                            # X-Y данные
    xy = models.TextField('Полученные данные x,y')
    measurement_data = models.ForeignKey(Measure, on_delete = models.CASCADE,related_name = 'm')
    isvalid=models.IntegerField(default=0, verbose_name="Валидность")
    def __str__(self):
        return ' Измерения: {}'.format(self.measurement_data)

class Operator(models.Model):
    firstname = models.CharField(default="Александр", verbose_name="Имя оператора", max_length=50)
    lastname = models.CharField(default="Иванов", verbose_name="Фамилия оператора", max_length=50)
    accept_data=models.ForeignKey(AcceptData, null=True,blank=True, on_delete = models.CASCADE, related_name = 'operator_ad',verbose_name="Проведенные измерения")
    def __str__(self):
        return f'{self.firstname} {self.lastname}'




























