import matplotlib.pyplot as plt

# Воспользуемся паттерном Декоратор
# Мы просто будем добавлять водяной знак к нашим графикам
# Не слишком серьёзная функциональность, конечно — но структуру объектов мы не меняем


class AddWatermark:
    def __call__(self, graph):
        watermark_text = "Курсовая работа по ТПиИСРСИИ"
        # Добавляем подграфик для выравнивания водяного знака
        ax = graph.add_subplot(111)
        # И добавляем сам водяной знак
        ax.text(0.01, 0.99, watermark_text, fontsize=10, color='gray',
                alpha=0.5, ha='left', va='top', transform=ax.transAxes)
        return graph
