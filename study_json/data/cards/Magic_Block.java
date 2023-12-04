package cards;

import basemod.abstracts.CustomCard;
import com.megacrit.cardcrawl.actions.AbstractGameAction;
import com.megacrit.cardcrawl.actions.common.ApplyPowerAction;
import com.megacrit.cardcrawl.actions.common.GainBlockAction;
import com.megacrit.cardcrawl.cards.AbstractCard;
import com.megacrit.cardcrawl.characters.AbstractPlayer;
import com.megacrit.cardcrawl.core.AbstractCreature;
import com.megacrit.cardcrawl.core.CardCrawlGame;
import com.megacrit.cardcrawl.localization.CardStrings;
import com.megacrit.cardcrawl.monsters.AbstractMonster;
import com.megacrit.cardcrawl.powers.AbstractPower;
import com.megacrit.cardcrawl.powers.ArtifactPower;
import patches_cht.AbstractCardEnum;
import patches_cht.CardTagEnum;
import power.Lose_Memory_Power;
import power.Magic_ImpactPower;

public class Magic_Block extends CustomCard {
    private static final CardStrings cardStrings = CardCrawlGame.languagePack.getCardStrings("Magic_Block");
    public static final String ID = "Magic_Block";
    public static final int LOSE = 3;

    public Magic_Block() {
        super(ID, cardStrings.NAME, "img/cards_Chtholly/Magic_Block.png", 2, cardStrings.DESCRIPTION, CardType.SKILL, AbstractCardEnum.Chtho_COLOR, CardRarity.RARE, CardTarget.SELF);
        this.baseBlock = 4;
        this.baseMagicNumber = 3;
        this.magicNumber = this.baseMagicNumber;
        this.tags.add(CardTagEnum.Magic);
    }

    public void use(AbstractPlayer p, AbstractMonster m) {
        int count = 0;
        for (AbstractCard card : p.drawPile.group) {
            if (card.hasTag(CardTagEnum.Magic)) {
                count++;
            }
        }
        for (int i = 0; i < this.magicNumber + count; i++) {
            addToBot(new GainBlockAction(p, p, this.block));
        }
        addToBot(new ApplyPowerAction(p, p, new Magic_ImpactPower(p,-1)));
    }

    public void upgrade() {
        if (!this.upgraded) {
            upgradeName();
            upgradeBlock(1);
            this.rawDescription = cardStrings.UPGRADE_DESCRIPTION;
            initializeDescription();
        }
    }


    public AbstractCard makeCopy() {
        return new Magic_Block();
    }
}


