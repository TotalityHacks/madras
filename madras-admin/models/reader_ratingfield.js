'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('reader_ratingfield', {
    'type': {
      type: DataTypes.STRING,
    },
    'prompt': {
      type: DataTypes.STRING,
    },
    'min_number': {
      type: DataTypes.INTEGER,
    },
    'max_number': {
      type: DataTypes.INTEGER,
    },
    'options': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'reader_ratingfield',
    underscored: true,
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.reader_rating, {
      foreignKey: 'rating_id',
      
      as: '_rating_id',
    });
    
  };

  return Model;
};

