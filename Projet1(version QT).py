import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QPushButton, 
                             QScrollArea, QFrame, QProgressBar, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QColor, QPalette, QPainter, QLinearGradient, QBrush, QPen

class GradientLabel(QLabel):
    """Label personnalisé avec effet de dégradé sur le texte"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Créer un dégradé
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#ff6b9d"))
        gradient.setColorAt(0.5, QColor("#c44569"))
        gradient.setColorAt(1, QColor("#a55eea"))
        
        # Dessiner le texte avec le dégradé
        painter.setPen(QPen(QBrush(gradient), 1))
        font = QFont('Nunito', 32, QFont.Bold)
        painter.setFont(font)
        
        # Centrer le texte
        rect = QRect(0, 0, self.width(), self.height())
        painter.drawText(rect, Qt.AlignCenter, self.text())

class LearningStylePredictor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Découvre Ton Style d'Apprentissage")
        self.setGeometry(100, 100, 1000, 800)
        
        # Permettre le redimensionnement
        self.setMinimumSize(900, 700)
        
        # Couleurs pastel
        self.colors = {
            'background': '#fffbeb',
            'header_gradient': ['#ffeef8', '#e3d5ff', '#d5f4ff'],
            'border': '#fbbf24',
            'card_visuel': ['#e0f2fe', '#ddd6fe'],
            'card_auditif': ['#f3e8ff', '#fce7f3'],
            'card_kinesthesique': ['#ffedd5', '#fed7aa'],
            'card_lecture': ['#d1fae5', '#a7f3d0']
        }
        
        # Initialisation des réponses
        self.answers = {
            'q1': 5, 'q2': 37.5, 'q3': 5, 'q4': 5,
            'q5': 6, 'q6': 5.5, 'q7': 5.5, 'q8': 5.5
        }
        
        # Informations sur les styles
        self.styles_info = {
            'Visuel': {
                'color': '#3b82f6',
                'border_color': '#93c5fd',
                'emoji': '👁️',
                'description': 'Tu es un(e) apprenant(e) VISUEL(LE) - Les images parlent plus que les mots !',
                'forces': [
                    '🎨 Excellente mémoire visuelle et spatiale',
                    '📊 Compréhension rapide des graphiques et schémas',
                    '🌈 Sensibilité aux couleurs et à l\'organisation visuelle',
                    '🎬 Apprentissage efficace avec vidéos et animations'
                ],
                'techniques': [
                    '📝 Utilise des mind maps (cartes mentales) colorées',
                    '🖍️ Surligne tes textes avec un code couleur',
                    '📹 Regarde des vidéos éducatives YouTube',
                    '📊 Crée des diagrammes et infographies',
                    '🎨 Dessine tes concepts pour mieux les retenir',
                    '💡 Utilise des flashcards illustrées'
                ],
                'outils': [
                    '• Canva, MindMeister (mind maps)',
                    '• YouTube, Khan Academy (vidéos)',
                    '• Notion, Evernote (organisation visuelle)',
                    '• Quizlet (flashcards visuelles)'
                ]
            },
            'Auditif': {
                'color': '#a855f7',
                'border_color': '#d8b4fe',
                'emoji': '🎧',
                'description': 'Tu es un(e) apprenant(e) AUDITIF(VE) - Tes oreilles sont ton meilleur atout !',
                'forces': [
                    '👂 Excellente mémoire auditive',
                    '🗣️ Apprentissage optimal par discussion',
                    '🎵 Sensibilité aux rythmes et mélodies',
                    '💬 Compréhension rapide des explications orales'
                ],
                'techniques': [
                    '🎙️ Enregistre tes cours et réécoute-les',
                    '🗣️ Explique à voix haute ce que tu apprends',
                    '👥 Participe à des groupes de discussion',
                    '🎧 Écoute des podcasts éducatifs',
                    '🎵 Crée des chansons/rimes pour mémoriser',
                    '📱 Utilise des applications text-to-speech'
                ],
                'outils': [
                    '• Spotify, Apple Podcasts (podcasts éducatifs)',
                    '• Voice Recorder (enregistrements)',
                    '• Discord, Zoom (discussions de groupe)',
                    '• Audible (livres audio)'
                ]
            },
            'Kinesthésique': {
                'color': '#f97316',
                'border_color': '#fdba74',
                'emoji': '✋',
                'description': 'Tu es un(e) apprenant(e) KINESTHÉSIQUE - Tu apprends en FAISANT !',
                'forces': [
                    '🏃 Apprentissage par l\'action et le mouvement',
                    '🔧 Excellence dans les travaux pratiques',
                    '🎯 Compréhension par expérimentation',
                    '💪 Énergie et dynamisme pendant l\'étude'
                ],
                'techniques': [
                    '🚶 Étudie en marchant ou bougeant',
                    '✍️ Écris physiquement (pas sur ordinateur)',
                    '🔬 Fais des expériences pratiques',
                    '🎭 Utilise des jeux de rôle pour apprendre',
                    '🏋️ Prends des pauses actives fréquentes',
                    '🧩 Manipule des objets physiques'
                ],
                'outils': [
                    '• Applications AR/VR pour apprentissage',
                    '• Laboratoires virtuels (PhET, Labster)',
                    '• Jeux éducatifs interactifs',
                    '• Escape games pédagogiques'
                ]
            },
            'Lecture-Écriture': {
                'color': '#10b981',
                'border_color': '#6ee7b7',
                'emoji': '📚',
                'description': 'Tu es un(e) apprenant(e) LECTURE-ÉCRITURE - Les mots sont ton pouvoir !',
                'forces': [
                    '📖 Excellente compréhension écrite',
                    '✍️ Mémorisation par l\'écriture',
                    '📝 Organisation textuelle naturelle',
                    '📚 Amour de la lecture et recherche'
                ],
                'techniques': [
                    '📓 Prends des notes détaillées manuscrites',
                    '📝 Réécris tes cours avec tes propres mots',
                    '📚 Lis des livres et articles complémentaires',
                    '✏️ Crée des fiches de révision écrites',
                    '📋 Fais des listes et des résumés',
                    '💭 Tiens un journal d\'apprentissage'
                ],
                'outils': [
                    '• Microsoft Word, Google Docs (prise de notes)',
                    '• Notion, Obsidian (organisation textuelle)',
                    '• Kindle, Pocket (lecture)',
                    '• Grammarly (amélioration écriture)'
                ]
            }
        }
        
        # Questions
        self.questions = [
            {
                'id': 'q1',
                'emoji': '🌅',
                'title': 'À quel moment es-tu le plus productif(ve) ?',
                'help': 'Choisis la période où tu te sens le plus alerte',
                'options': [
                    ('🌅 Tôt le matin (6h-9h)', 2),
                    ('☀️ Matinée (9h-12h)', 4),
                    ('🌤️ Début après-midi (12h-15h)', 5),
                    ('🌆 Fin après-midi (15h-18h)', 7),
                    ('🌃 Soirée (18h-22h)', 9),
                    ('🌙 Nuit (22h-2h)', 10)
                ]
            },
            {
                'id': 'q2',
                'emoji': '⏱️',
                'title': 'Durée de concentration maximale sans pause ?',
                'help': 'Temps avant que ton attention diminue',
                'options': [
                    ('⚡ 15-20 minutes', 17.5),
                    ('🔋 20-30 minutes', 25),
                    ('💪 30-45 minutes', 37.5),
                    ('🎯 45-60 minutes', 52.5),
                    ('🏆 60-90 minutes', 75),
                    ('🌟 Plus de 90 minutes', 105)
                ]
            },
            {
                'id': 'q3',
                'emoji': '🎵',
                'title': 'Dans quel environnement études-tu le mieux ?',
                'help': 'L\'ambiance sonore qui favorise ta concentration',
                'options': [
                    ('🤫 Silence total absolu', 1),
                    ('📚 Bibliothèque calme', 2.5),
                    ('🎵 Musique douce / instrumentale', 5),
                    ('☕ Café avec bruit de fond', 6.5),
                    ('🗣️ Environnement avec conversations', 8),
                    ('🎉 Ambiance animée', 9)
                ]
            },
            {
                'id': 'q4',
                'emoji': '👥',
                'title': 'Comment préfères-tu étudier ?',
                'help': 'Ton mode préféré d\'interaction sociale',
                'options': [
                    ('🧘 Seul(e), isolé(e)', 1),
                    ('👤 Seul(e) mais pas isolé(e)', 2.5),
                    ('👥 Avec 1-2 personnes', 5),
                    ('👨‍👩‍👧 Petit groupe (3-5)', 7),
                    ('👨‍👩‍👧‍👦 Grand groupe (6+)', 9)
                ]
            },
            {
                'id': 'q5',
                'emoji': '💡',
                'title': 'Comment apprends-tu le mieux un nouveau concept ?',
                'help': 'La méthode qui te fait comprendre le plus vite',
                'options': [
                    ('📖 En lisant des textes', 2),
                    ('👂 En écoutant des explications', 3.5),
                    ('📊 En voyant des schémas/images', 6),
                    ('🎬 En regardant des vidéos', 7),
                    ('✍️ En pratiquant / faisant', 8.5),
                    ('🔧 En expérimentant librement', 9.5)
                ]
            },
            {
                'id': 'q6',
                'emoji': '📋',
                'title': 'Quel est ton niveau d\'organisation ?',
                'help': 'Comment gères-tu tes études au quotidien',
                'options': [
                    ('🌪️ Chaos créatif', 2),
                    ('🎭 Désorganisé(e) mais ça marche', 3.5),
                    ('⚖️ Équilibre / flexible', 5.5),
                    ('📋 Plutôt organisé(e)', 7),
                    ('🗂️ Très organisé(e)', 8.5),
                    ('📅 Planning strict et détaillé', 9.5)
                ]
            },
            {
                'id': 'q7',
                'emoji': '☕',
                'title': 'À quelle fréquence prends-tu des pauses ?',
                'help': 'Ton rythme naturel de travail',
                'options': [
                    ('🔒 Rarement, je travaille longtemps', 2),
                    ('⏱️ Toutes les heures', 4),
                    ('⏰ Toutes les 45 minutes', 5.5),
                    ('📍 Toutes les 30 minutes', 7),
                    ('⚡ Toutes les 20 minutes', 8.5),
                    ('🔄 Très souvent (10-15 min)', 9.5)
                ]
            },
            {
                'id': 'q8',
                'emoji': '💻',
                'title': 'Quel support utilises-tu pour étudier ?',
                'help': 'Tes outils préférés pour apprendre',
                'options': [
                    ('📝 Papier et stylo uniquement', 1.5),
                    ('📔 Principalement papier', 3),
                    ('⚖️ Moitié papier / moitié digital', 5.5),
                    ('💻 Principalement digital', 7.5),
                    ('📱 Tablette / smartphone', 8.5),
                    ('🖥️ 100% digital et outils en ligne', 9.5)
                ]
            }
        ]
        
        self.combos = {}
        self.init_ui()
    
    def init_ui(self):
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Appliquer le fond pastel
        main_widget.setStyleSheet(f"background-color: {self.colors['background']};")
        
        # Zone de défilement vertical uniquement
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Désactiver défilement horizontal
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #c084fc;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a855f7;
            }
        """)
        
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setSpacing(20)
        
        # En-tête avec gradient pastel
        header = QFrame()
        header.setMinimumHeight(180)
        header.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 {self.colors['header_gradient'][0]}, 
                stop:0.5 {self.colors['header_gradient'][1]}, 
                stop:1 {self.colors['header_gradient'][2]});
            border-radius: 30px;
            padding: 30px;
        """)
        
        # Ajouter un effet d'ombre
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(255, 182, 193, 100))
        shadow.setOffset(0, 10)
        header.setGraphicsEffect(shadow)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Emoji
        emoji_label = QLabel("🧠✨")
        emoji_label.setFont(QFont('Arial', 50))
        emoji_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(emoji_label)
        
        # Titre avec dégradé personnalisé
        title_label = GradientLabel("Découvre Ton Style d'Apprentissage")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setMinimumHeight(40)
        header_layout.addWidget(title_label)
        
        # Sous-titre
        subtitle = QLabel("✨ Un voyage personnalisé vers l'apprentissage optimal ✨")
        subtitle.setFont(QFont('Arial', 14, QFont.Bold))
        subtitle.setStyleSheet("color: #7d5ba6;")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)
        
        # Carte d'information
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #fff5f7, stop:1 #ffe8f0);
            border: 3px solid #ffc2d9;
            border-radius: 25px;
            padding: 20px;
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        
        info_title = QLabel("🌸 Qu'est-ce qu'un style d'apprentissage ?")
        info_title.setFont(QFont('Arial', 16, QFont.Bold))
        info_title.setStyleSheet("color: #d946a6;")
        info_layout.addWidget(info_title)
        
        info_text = QLabel(
            "Chaque personne apprend différemment ! Ce système identifie ton style optimal parmi :<br><br>"
            "<span style='background: linear-gradient(135deg, #bfdbfe 0%, #ddd6fe 100%); "
            "color: #3b82f6; padding: 6px 12px; border-radius: 12px; font-weight: bold; font-size: 11px;'>👁️ VISUEL</span> "
            "<span style='background: linear-gradient(135deg, #e9d5ff 0%, #fbcfe8 100%); "
            "color: #a855f7; padding: 6px 12px; border-radius: 12px; font-weight: bold; font-size: 11px;'>🎧 AUDITIF</span> "
            "<span style='background: linear-gradient(135deg, #fed7aa 0%, #fde68a 100%); "
            "color: #f97316; padding: 6px 12px; border-radius: 12px; font-weight: bold; font-size: 11px;'>✋ KINESTHÉSIQUE</span> "
            "<span style='background: linear-gradient(135deg, #a7f3d0 0%, #bfdbfe 100%); "
            "color: #10b981; padding: 6px 12px; border-radius: 12px; font-weight: bold; font-size: 11px;'>📚 LECTURE-ÉCRITURE</span><br><br>"
            "<strong>💡 Pourquoi c'est important ?</strong> Connaître ton style te permet d'adapter "
            "tes méthodes d'étude et de maximiser ton efficacité !"
        )
        info_text.setFont(QFont('Arial', 10))
        info_text.setStyleSheet("color: #6b5b7a;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_frame)
        
        # Section questionnaire
        section_header = QFrame()
        section_header.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #fbbf24, stop:1 #f59e0b);
            border-radius: 20px;
            padding: 15px;
        """)
        section_layout = QVBoxLayout(section_header)
        
        section_label = QLabel("📝 Réponds à 8 questions sur tes habitudes")
        section_label.setFont(QFont('Arial', 18, QFont.Bold))
        section_label.setStyleSheet("color: white;")
        section_label.setAlignment(Qt.AlignCenter)
        section_layout.addWidget(section_label)
        
        layout.addWidget(section_header)
        
        # Créer les questions
        for question in self.questions:
            q_frame = QFrame()
            q_frame.setStyleSheet("""
                background: white;
                border-left: 6px solid #b794f6;
                border-radius: 20px;
                padding: 15px;
            """)
            q_layout = QVBoxLayout(q_frame)
            q_layout.setContentsMargins(10, 10, 10, 10)
            
            # Numéro et emoji
            header_layout = QHBoxLayout()
            number_label = QLabel(f"Question {self.questions.index(question) + 1}")
            number_label.setFont(QFont('Arial', 12, QFont.Bold))
            number_label.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #ffd6e8, stop:1 #c7b9ff);
                color: #7c3aed;
                padding: 6px 12px;
                border-radius: 12px;
            """)
            header_layout.addWidget(number_label)
            
            emoji_label = QLabel(question['emoji'])
            emoji_label.setFont(QFont('Arial', 16))
            header_layout.addWidget(emoji_label)
            header_layout.addStretch()
            
            q_layout.addLayout(header_layout)
            
            # Titre de la question
            q_label = QLabel(question['title'])
            q_label.setFont(QFont('Arial', 12, QFont.Bold))
            q_label.setStyleSheet("color: #4a3b5f; margin-top: 5px;")
            q_label.setWordWrap(True)
            q_layout.addWidget(q_label)
            
            # Aide
            q_help = QLabel(question['help'])
            q_help.setFont(QFont('Arial', 10))
            q_help.setStyleSheet("color: #8b7c9e; font-style: italic; margin-bottom: 10px;")
            q_help.setWordWrap(True)
            q_layout.addWidget(q_help)
            
            # Combo box
            combo = QComboBox()
            combo.setFont(QFont('Arial', 10))
            combo.setStyleSheet("""
                QComboBox {
                    padding: 10px;
                    border: 2px solid #D1D5DB;
                    border-radius: 8px;
                    background: white;
                    min-height: 40px;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 30px;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 5px solid transparent;
                    border-right: 5px solid transparent;
                    border-top: 8px solid #6b7280;
                }
                QComboBox QAbstractItemView {
                    border: 2px solid #D1D5DB;
                    border-radius: 8px;
                    selection-background-color: #f3f4f6;
                    padding: 5px;
                }
            """)
            
            for label, value in question['options']:
                combo.addItem(label, value)
            
            # Sélectionner la valeur par défaut
            default_val = self.answers[question['id']]
            for i, (_, val) in enumerate(question['options']):
                if val == default_val:
                    combo.setCurrentIndex(i)
                    break
            
            combo.currentIndexChanged.connect(lambda idx, qid=question['id'], cb=combo: 
                                             self.update_answer(qid, cb.currentData()))
            
            self.combos[question['id']] = combo
            q_layout.addWidget(combo)
            
            layout.addWidget(q_frame)
        
        # Boutons avec style pastel
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.setContentsMargins(0, 10, 0, 10)
        
        self.predict_btn = QPushButton("✨ DÉCOUVRIR MON STYLE")
        self.predict_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.predict_btn.setMinimumHeight(60)
        self.predict_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #c084fc, stop:1 #a855f7);
                color: white;
                border-radius: 15px;
                padding: 15px 25px;
                border: none;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #a855f7, stop:1 #9333ea);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9333ea, stop:1 #7c3aed);
            }
        """)
        self.predict_btn.clicked.connect(self.predict_style)
        btn_layout.addWidget(self.predict_btn)
        
        self.reset_btn = QPushButton("🔄 RECOMMENCER")
        self.reset_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.reset_btn.setMinimumHeight(60)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #fbbf24, stop:1 #f59e0b);
                color: white;
                border-radius: 15px;
                padding: 15px 25px;
                border: none;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f59e0b, stop:1 #d97706);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d97706, stop:1 #b45309);
            }
        """)
        self.reset_btn.clicked.connect(self.reset_form)
        btn_layout.addWidget(self.reset_btn)
        
        layout.addLayout(btn_layout)
        
        # Zone de résultats
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        self.results_widget.hide()
        layout.addWidget(self.results_widget)
        
        # Footer
        footer = QFrame()
        footer.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #fce7f3, stop:1 #e0e7ff);
            border-radius: 20px;
            padding: 20px;
        """)
        footer_layout = QVBoxLayout(footer)
        
        footer_label = QLabel("✨ Fait avec amour pour optimiser ton apprentissage ✨<br>Bonne découverte de ton style !")
        footer_label.setFont(QFont('Arial', 12, QFont.Bold))
        footer_label.setStyleSheet("color: #7c3aed;")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setWordWrap(True)
        footer_layout.addWidget(footer_label)
        
        layout.addWidget(footer)
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
    
    def update_answer(self, qid, value):
        self.answers[qid] = value
    
    def predict_style(self):
        features = [
            self.answers['q1'], self.answers['q2'], self.answers['q3'], self.answers['q4'],
            self.answers['q5'], self.answers['q6'], self.answers['q7'], self.answers['q8']
        ]
        
        scores = {'Visuel': 0, 'Auditif': 0, 'Kinesthésique': 0, 'Lecture-Écriture': 0}
        
        # Algorithme de prédiction
        if features[0] < 4:
            scores['Auditif'] += 2
            scores['Lecture-Écriture'] += 2
        elif features[0] < 7:
            scores['Visuel'] += 3
        else:
            scores['Kinesthésique'] += 3
        
        if features[1] < 30:
            scores['Kinesthésique'] += 3
        elif features[1] > 60:
            scores['Lecture-Écriture'] += 3
        else:
            scores['Visuel'] += 2
            scores['Auditif'] += 2
        
        if features[2] < 3:
            scores['Lecture-Écriture'] += 3
        elif features[2] > 6:
            scores['Auditif'] += 3
            scores['Kinesthésique'] += 2
        else:
            scores['Visuel'] += 2
        
        if features[3] < 4:
            scores['Lecture-Écriture'] += 3
            scores['Visuel'] += 1
        else:
            scores['Auditif'] += 3
            scores['Kinesthésique'] += 3
        
        if features[4] < 3.5:
            scores['Lecture-Écriture'] += 4
        elif features[4] < 5:
            scores['Auditif'] += 4
        elif features[4] < 7.5:
            scores['Visuel'] += 4
        else:
            scores['Kinesthésique'] += 4
        
        if features[5] < 4:
            scores['Kinesthésique'] += 2
        elif features[5] > 7:
            scores['Lecture-Écriture'] += 3
        else:
            scores['Visuel'] += 1
            scores['Auditif'] += 1
        
        if features[6] < 4:
            scores['Lecture-Écriture'] += 2
        elif features[6] > 7:
            scores['Kinesthésique'] += 3
        else:
            scores['Visuel'] += 1
            scores['Auditif'] += 1
        
        if features[7] < 4:
            scores['Lecture-Écriture'] += 2
        elif features[7] > 7:
            scores['Visuel'] += 3
        else:
            scores['Auditif'] += 1
            scores['Kinesthésique'] += 1
        
        total = sum(scores.values())
        probabilities = {k: (v / total) * 100 for k, v in scores.items()}
        predicted_style = max(scores, key=scores.get)
        
        self.show_results(predicted_style, probabilities)
    
    def show_results(self, style, probabilities):
        # Nettoyer les anciens résultats
        for i in reversed(range(self.results_layout.count())):
            self.results_layout.itemAt(i).widget().setParent(None)
        
        info = self.styles_info[style]
        
        # Résultat principal
        result_frame = QFrame()
        result_frame.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 {self.colors[f'card_{style.lower().replace("é", "e").replace("è", "e")}'.split('-')[0]][0]}, 
                stop:1 {self.colors[f'card_{style.lower().replace("é", "e").replace("è", "e")}'.split('-')[0]][1]});
            border: 5px solid {info['border_color']};
            border-radius: 25px;
            padding: 30px;
        """)
        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(20, 20, 20, 20)
        
        emoji_label = QLabel(info['emoji'])
        emoji_label.setFont(QFont('Arial', 60))
        emoji_label.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(emoji_label)
        
        style_label = QLabel(style.upper())
        style_label.setFont(QFont('Arial', 32, QFont.Bold))
        style_label.setStyleSheet(f"color: {info['color']};")
        style_label.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(style_label)
        
        desc_label = QLabel(info['description'])
        desc_label.setFont(QFont('Arial', 14, QFont.Bold))
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet(f"color: {info['color']};")
        result_layout.addWidget(desc_label)
        
        conf_label = QLabel(f"🎯 Confiance : {probabilities[style]:.1f}%")
        conf_label.setFont(QFont('Arial', 13, QFont.Bold))
        conf_label.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(conf_label)
        
        self.results_layout.addWidget(result_frame)
        
        # Forces
        forces_frame = QFrame()
        forces_frame.setStyleSheet("""
            background: white;
            border-radius: 20px;
            padding: 20px;
        """)
        forces_layout = QVBoxLayout(forces_frame)
        
        forces_title = QLabel(f"✨ Tes Forces Naturelles :")
        forces_title.setFont(QFont('Arial', 18, QFont.Bold))
        forces_title.setStyleSheet(f"color: {info['color']};")
        forces_layout.addWidget(forces_title)
        
        for force in info['forces']:
            f_label = QLabel(force)
            f_label.setFont(QFont('Arial', 11))
            f_label.setWordWrap(True)
            f_label.setStyleSheet("margin: 8px 0; padding-left: 10px;")
            forces_layout.addWidget(f_label)
        
        self.results_layout.addWidget(forces_frame)
        
        # Techniques
        tech_frame = QFrame()
        tech_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #fef3c7, stop:1 #fde68a);
            border-radius: 20px;
            padding: 20px;
        """)
        tech_layout = QVBoxLayout(tech_frame)
        
        tech_title = QLabel("🎯 Techniques Recommandées :")
        tech_title.setFont(QFont('Arial', 18, QFont.Bold))
        tech_title.setStyleSheet("color: #d97706;")
        tech_layout.addWidget(tech_title)
        
        for i, tech in enumerate(info['techniques'], 1):
            t_label = QLabel(f"<strong>{i}.</strong> {tech}")
            t_label.setFont(QFont('Arial', 11))
            t_label.setWordWrap(True)
            t_label.setTextFormat(Qt.RichText)
            t_label.setStyleSheet("margin: 8px 0; padding-left: 10px;")
            tech_layout.addWidget(t_label)
        
        self.results_layout.addWidget(tech_frame)
        
        # Outils
        outils_frame = QFrame()
        outils_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #e0e7ff, stop:1 #c7d2fe);
            border-radius: 20px;
            padding: 20px;
        """)
        outils_layout = QVBoxLayout(outils_frame)
        
        outils_title = QLabel("🛠 Outils Recommandés")
        outils_title.setFont(QFont('Arial', 18, QFont.Bold))
        outils_title.setStyleSheet("color: #4f46e5;")
        outils_layout.addWidget(outils_title)
        
        for outil in info['outils']:
            o_label = QLabel(outil)
            o_label.setFont(QFont('Arial', 11))
            o_label.setWordWrap(True)
            o_label.setStyleSheet("margin: 6px 0; padding-left: 10px;")
            outils_layout.addWidget(o_label)
        
        self.results_layout.addWidget(outils_frame)
        
        # Distribution
        dist_frame = QFrame()
        dist_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #ddd6fe, stop:1 #c4b5fd);
            border-radius: 20px;
            padding: 20px;
        """)
        dist_layout = QVBoxLayout(dist_frame)
        
        dist_title = QLabel("📊 Distribution de Tes Styles")
        dist_title.setFont(QFont('Arial', 18, QFont.Bold))
        dist_title.setStyleSheet("color: #7c3aed;")
        dist_layout.addWidget(dist_title)
        
        for s, prob in probabilities.items():
            s_layout = QVBoxLayout()
            
            s_label = QLabel(f"{s}: {prob:.1f}%")
            s_label.setFont(QFont('Arial', 11, QFont.Bold))
            s_label.setStyleSheet(f"color: {self.styles_info[s]['color']};")
            s_layout.addWidget(s_label)
            
            progress = QProgressBar()
            progress.setMaximum(100)
            progress.setValue(int(prob))
            progress.setTextVisible(False)
            progress.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    border-radius: 5px;
                    background-color: #D1D5DB;
                    height: 18px;
                }}
                QProgressBar::chunk {{
                    background-color: {self.styles_info[s]['color']};
                    border-radius: 5px;
                }}
            """)
            s_layout.addWidget(progress)
            
            dist_layout.addLayout(s_layout)
        
        self.results_layout.addWidget(dist_frame)
        
        # Conseil final
        conseil_frame = QFrame()
        conseil_frame.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 {self.colors['header_gradient'][0]}, 
                stop:1 {self.colors['header_gradient'][1]});
            border-radius: 20px;
            padding: 20px;
        """)
        conseil_layout = QVBoxLayout(conseil_frame)
        
        conseil_title = QLabel("💡 Conseil Final")
        conseil_title.setFont(QFont('Arial', 18, QFont.Bold))
        conseil_title.setStyleSheet("color: #d946a6;")
        conseil_layout.addWidget(conseil_title)
        
        conseil_text = QLabel(
            "Bien que tu aies un style dominant, <strong>la meilleure stratégie</strong> est de "
            "<strong>combiner plusieurs approches</strong> ! Adapte tes méthodes selon les matières "
            "et n'hésite pas à expérimenter. L'apprentissage est personnel et évolutif. 🚀"
        )
        conseil_text.setFont(QFont('Arial', 11))
        conseil_text.setStyleSheet("color: #6b5b7a;")
        conseil_text.setWordWrap(True)
        conseil_text.setTextFormat(Qt.RichText)
        conseil_layout.addWidget(conseil_text)
        
        self.results_layout.addWidget(conseil_frame)
        
        self.results_widget.show()
    
    def reset_form(self):
        self.answers = {
            'q1': 5, 'q2': 37.5, 'q3': 5, 'q4': 5,
            'q5': 6, 'q6': 5.5, 'q7': 5.5, 'q8': 5.5
        }
        
        for qid, combo in self.combos.items():
            default_val = self.answers[qid]
            for i in range(combo.count()):
                if combo.itemData(i) == default_val:
                    combo.setCurrentIndex(i)
                    break
        
        self.results_widget.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Définir la police par défaut
    font = QFont('Arial', 10)
    app.setFont(font)
    
    window = LearningStylePredictor()
    window.show()
    sys.exit(app.exec_())